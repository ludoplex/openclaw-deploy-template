#!/usr/bin/env node
/**
 * Capture Subagent Transcripts
 * 
 * Usage: node capture-subagent-transcripts.js <agentId> [sessionId]
 * 
 * If sessionId not provided, captures the most recent session for that agent.
 * Outputs to memory/agent-transcripts/
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const crypto = require('crypto');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace');
const AGENTS_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'agents');
const TRANSCRIPT_DIR = path.join(WORKSPACE, 'memory', 'agent-transcripts');
const MANIFEST_PATH = path.join(TRANSCRIPT_DIR, '.manifest.json');

/**
 * Compute SHA256 hash of content
 */
function computeHash(content) {
  return crypto.createHash('sha256').update(content).digest('hex');
}

/**
 * Load or initialize manifest
 */
function loadManifest() {
  if (fs.existsSync(MANIFEST_PATH)) {
    return JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf8'));
  }
  return { version: "1.0", description: "Integrity manifest for agent transcripts", entries: {} };
}

/**
 * Save manifest
 */
function saveManifest(manifest) {
  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2));
}

/**
 * Add entry to manifest with hash and metadata
 */
function addToManifest(filename, content, agentId, sessionId) {
  const manifest = loadManifest();
  const hash = computeHash(content);
  const timestamp = new Date().toISOString();
  
  manifest.entries[filename] = {
    sha256: hash,
    capturedAt: timestamp,
    agentId: agentId,
    sessionId: sessionId,
    size: content.length
  };
  
  saveManifest(manifest);
  return hash;
}

async function parseSessionTranscript(jsonlPath) {
  const content = {
    metadata: null,
    messages: [],
    thinking: [],
    toolCalls: []
  };

  const fileStream = fs.createReadStream(jsonlPath);
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

  for await (const line of rl) {
    if (!line.trim()) continue;
    try {
      const entry = JSON.parse(line);
      
      if (entry.type === 'session') {
        content.metadata = { id: entry.id, timestamp: entry.timestamp, cwd: entry.cwd };
      }
      
      if (entry.type === 'message' && entry.message) {
        const msg = entry.message;
        if (Array.isArray(msg.content)) {
          for (const block of msg.content) {
            if (block.type === 'thinking' && block.thinking) {
              content.thinking.push({ timestamp: entry.timestamp, text: block.thinking });
            }
            if (block.type === 'text' && block.text) {
              content.messages.push({ role: msg.role, timestamp: entry.timestamp, text: block.text });
            }
            if (block.type === 'toolCall') {
              content.toolCalls.push({ timestamp: entry.timestamp, name: block.name, arguments: block.arguments });
            }
          }
        }
        if (msg.role === 'toolResult' && msg.content) {
          const lastTC = content.toolCalls[content.toolCalls.length - 1];
          if (lastTC) {
            lastTC.result = Array.isArray(msg.content) ? msg.content.map(c => c.text || '').join('\n') : String(msg.content);
          }
        }
      }
    } catch (e) { /* skip */ }
  }
  return content;
}

function formatMarkdown(content, agentId) {
  let md = `# Subagent Transcript: ${agentId}\n\n`;
  md += `**Session ID:** ${content.metadata?.id || 'unknown'}\n`;
  md += `**Started:** ${content.metadata?.timestamp || 'unknown'}\n\n---\n\n`;

  if (content.thinking.length > 0) {
    md += `## Reasoning (Thinking Blocks)\n\n`;
    for (const t of content.thinking) {
      md += `### ${t.timestamp}\n\`\`\`\n${t.text}\n\`\`\`\n\n`;
    }
  }

  if (content.toolCalls.length > 0) {
    md += `## Tool Calls\n\n`;
    for (const tc of content.toolCalls) {
      md += `### ${tc.name}\n`;
      md += `**Args:** \`${JSON.stringify(tc.arguments).substring(0, 200)}...\`\n`;
      if (tc.result) {
        const preview = tc.result.length > 1000 ? tc.result.substring(0, 1000) + '...[truncated]' : tc.result;
        md += `**Result:**\n\`\`\`\n${preview}\n\`\`\`\n`;
      }
      md += '\n';
    }
  }

  if (content.messages.length > 0) {
    md += `## Messages\n\n`;
    for (const m of content.messages) {
      md += `**[${m.role}]** ${m.timestamp}\n${m.text}\n\n---\n\n`;
    }
  }

  return md;
}

async function main() {
  const agentId = process.argv[2];
  const sessionId = process.argv[3];

  if (!agentId) {
    console.error('Usage: node capture-subagent-transcripts.js <agentId> [sessionId]');
    process.exit(1);
  }

  const sessionsDir = path.join(AGENTS_DIR, agentId, 'sessions');
  if (!fs.existsSync(sessionsDir)) {
    console.error(`No sessions directory for agent: ${agentId}`);
    process.exit(1);
  }

  // Find session file
  const files = fs.readdirSync(sessionsDir)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => ({ name: f, path: path.join(sessionsDir, f), mtime: fs.statSync(path.join(sessionsDir, f)).mtime }))
    .sort((a, b) => b.mtime - a.mtime);

  let sessionFile = sessionId ? files.find(f => f.name.includes(sessionId)) : files[0];
  if (!sessionFile) {
    console.error('Session file not found');
    process.exit(1);
  }

  console.log(`Parsing: ${sessionFile.path}`);
  const content = await parseSessionTranscript(sessionFile.path);
  const markdown = formatMarkdown(content, agentId);

  // Ensure output dir
  if (!fs.existsSync(TRANSCRIPT_DIR)) {
    fs.mkdirSync(TRANSCRIPT_DIR, { recursive: true });
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  const filename = `${agentId}-${timestamp}.md`;
  const outFile = path.join(TRANSCRIPT_DIR, filename);
  fs.writeFileSync(outFile, markdown);
  
  // Add to manifest with hash
  const hash = addToManifest(filename, markdown, agentId, content.metadata?.id || 'unknown');
  console.log(`Transcript saved: ${outFile}`);
  console.log(`SHA256: ${hash}`);
  console.log(`Manifest updated: ${MANIFEST_PATH}`);
}

/**
 * Verify integrity of all transcripts against manifest
 */
async function verify() {
  const manifest = loadManifest();
  let valid = 0, invalid = 0, missing = 0;
  
  console.log('Verifying transcript integrity...\n');
  
  for (const [filename, meta] of Object.entries(manifest.entries)) {
    const filePath = path.join(TRANSCRIPT_DIR, filename);
    
    if (!fs.existsSync(filePath)) {
      console.log(`❌ MISSING: ${filename}`);
      missing++;
      continue;
    }
    
    const content = fs.readFileSync(filePath, 'utf8');
    const currentHash = computeHash(content);
    
    if (currentHash === meta.sha256) {
      console.log(`✅ VALID: ${filename}`);
      valid++;
    } else {
      console.log(`❌ MODIFIED: ${filename}`);
      console.log(`   Expected: ${meta.sha256}`);
      console.log(`   Current:  ${currentHash}`);
      invalid++;
    }
  }
  
  console.log(`\nSummary: ${valid} valid, ${invalid} modified, ${missing} missing`);
  
  if (invalid > 0 || missing > 0) {
    process.exit(1);
  }
}

// Main entry point
if (process.argv[2] === '--verify') {
  verify().catch(console.error);
} else {
  main().catch(console.error);
}
