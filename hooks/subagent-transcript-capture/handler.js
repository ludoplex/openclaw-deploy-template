/**
 * Subagent Transcript Capture Hook
 * 
 * Automatically extracts and saves human-readable transcripts from subagent sessions.
 * Captures reasoning (thinking blocks), tool calls, outputs, and inter-agent discourse.
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const TRANSCRIPT_DIR = 'memory/agent-transcripts';

/**
 * Parse a JSONL session file and extract human-readable content
 */
async function parseSessionTranscript(jsonlPath) {
  const content = {
    metadata: null,
    messages: [],
    thinking: [],
    toolCalls: [],
    finalOutput: null
  };

  const fileStream = fs.createReadStream(jsonlPath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });

  for await (const line of rl) {
    if (!line.trim()) continue;
    
    try {
      const entry = JSON.parse(line);
      
      // Session metadata
      if (entry.type === 'session') {
        content.metadata = {
          id: entry.id,
          timestamp: entry.timestamp,
          cwd: entry.cwd
        };
      }
      
      // Messages with content
      if (entry.type === 'message' && entry.message) {
        const msg = entry.message;
        
        if (Array.isArray(msg.content)) {
          for (const block of msg.content) {
            // Thinking blocks
            if (block.type === 'thinking' && block.thinking) {
              content.thinking.push({
                timestamp: entry.timestamp,
                text: block.thinking
              });
            }
            
            // Text content
            if (block.type === 'text' && block.text) {
              content.messages.push({
                role: msg.role,
                timestamp: entry.timestamp,
                text: block.text
              });
              // Last assistant message is final output
              if (msg.role === 'assistant') {
                content.finalOutput = block.text;
              }
            }
            
            // Tool calls
            if (block.type === 'toolCall') {
              content.toolCalls.push({
                timestamp: entry.timestamp,
                name: block.name,
                arguments: block.arguments
              });
            }
          }
        }
        
        // Tool results
        if (msg.role === 'toolResult' && msg.content) {
          const lastToolCall = content.toolCalls[content.toolCalls.length - 1];
          if (lastToolCall) {
            lastToolCall.result = Array.isArray(msg.content) 
              ? msg.content.map(c => c.text || '').join('\n')
              : msg.content;
          }
        }
      }
    } catch (e) {
      // Skip malformed lines
    }
  }

  return content;
}

/**
 * Format parsed content as human-readable markdown
 */
function formatAsMarkdown(content, agentId, task) {
  let md = `# Subagent Transcript: ${agentId}\n\n`;
  md += `**Session ID:** ${content.metadata?.id || 'unknown'}\n`;
  md += `**Started:** ${content.metadata?.timestamp || 'unknown'}\n`;
  md += `**Task:** ${task || 'Not specified'}\n\n`;
  md += `---\n\n`;

  // Reasoning / Thinking
  if (content.thinking.length > 0) {
    md += `## Reasoning (Thinking Blocks)\n\n`;
    for (const t of content.thinking) {
      md += `### ${t.timestamp}\n`;
      md += `${t.text}\n\n`;
    }
    md += `---\n\n`;
  }

  // Tool Calls
  if (content.toolCalls.length > 0) {
    md += `## Tool Calls\n\n`;
    for (const tc of content.toolCalls) {
      md += `### ${tc.name} (${tc.timestamp})\n`;
      md += `**Arguments:**\n\`\`\`json\n${JSON.stringify(tc.arguments, null, 2)}\n\`\`\`\n`;
      if (tc.result) {
        const resultPreview = tc.result.length > 2000 
          ? tc.result.substring(0, 2000) + '\n... [truncated]'
          : tc.result;
        md += `**Result:**\n\`\`\`\n${resultPreview}\n\`\`\`\n`;
      }
      md += `\n`;
    }
    md += `---\n\n`;
  }

  // Final Output
  if (content.finalOutput) {
    md += `## Final Output\n\n`;
    md += content.finalOutput;
    md += `\n`;
  }

  return md;
}

/**
 * Main handler - capture transcript from a completed subagent session
 */
async function captureSubagentTranscript(sessionKey, agentId, task, workspaceDir) {
  // Ensure transcript directory exists
  const transcriptDir = path.join(workspaceDir, TRANSCRIPT_DIR);
  if (!fs.existsSync(transcriptDir)) {
    fs.mkdirSync(transcriptDir, { recursive: true });
  }

  // Parse session key to find JSONL file
  // Format: agent:{agentId}:subagent:{sessionId}
  const parts = sessionKey.split(':');
  const sessionId = parts[3] || parts[1];
  
  // Look for session file
  const agentSessionsDir = path.join(
    process.env.HOME || process.env.USERPROFILE,
    '.openclaw', 'agents', agentId, 'sessions'
  );

  if (!fs.existsSync(agentSessionsDir)) {
    console.error(`Sessions directory not found: ${agentSessionsDir}`);
    return null;
  }

  // Find the session file (might need to match by sessionId)
  const sessionFiles = fs.readdirSync(agentSessionsDir)
    .filter(f => f.endsWith('.jsonl'))
    .map(f => ({
      name: f,
      path: path.join(agentSessionsDir, f),
      mtime: fs.statSync(path.join(agentSessionsDir, f)).mtime
    }))
    .sort((a, b) => b.mtime - a.mtime);

  // Find matching session or use most recent
  let sessionFile = sessionFiles.find(f => f.name.includes(sessionId));
  if (!sessionFile && sessionFiles.length > 0) {
    sessionFile = sessionFiles[0]; // Most recent
  }

  if (!sessionFile) {
    console.error('No session file found');
    return null;
  }

  // Parse and format
  const content = await parseSessionTranscript(sessionFile.path);
  const markdown = formatAsMarkdown(content, agentId, task);

  // Save transcript
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  const filename = `${agentId}-${timestamp}.md`;
  const outputPath = path.join(transcriptDir, filename);
  
  fs.writeFileSync(outputPath, markdown);
  console.log(`Transcript saved: ${outputPath}`);
  
  return outputPath;
}

module.exports = { captureSubagentTranscript, parseSessionTranscript, formatAsMarkdown };
