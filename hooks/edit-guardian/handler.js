/**
 * Edit Guardian Hook
 * Enforces: 1) Read before edit, 2) Consult specialists for domain-specific files
 */

// Specialist routing table
const SPECIALIST_PATTERNS = [
  { pattern: /\.github\/workflows\//i, agents: ["cicd"], domain: "CI/CD workflows" },
  { pattern: /scripts\/build-.*\.(ps1|sh)$/i, agents: ["cicd", "testcov"], domain: "build scripts" },
  { pattern: /Makefile/i, agents: ["cicd", "cosmo"], domain: "build system" },
  { pattern: /tests?\//i, agents: ["testcov"], domain: "test files" },
  { pattern: /src\/db\//i, agents: ["ops"], domain: "database layer" },
  { pattern: /src\/(net|sync)\//i, agents: ["neteng"], domain: "network/sync" },
  { pattern: /helpers\/gui_/i, agents: ["cosmo", "asm"], domain: "platform helpers" },
  { pattern: /\.(asm|s)$/i, agents: ["asm"], domain: "assembly" },
  { pattern: /vendor\//i, agents: ["cosmo"], domain: "vendor dependencies" },
];

// Files exempt from read-before-edit rule
const EXEMPT_PATTERNS = [
  /AGENTS\.md$/i,
  /SOUL\.md$/i,
  /memory\//i,
  /HEARTBEAT\.md$/i,
  /\.gitignore$/i,
];

// Session state (persists across calls within session)
const sessionState = {
  filesRead: new Set(),
  filesCreated: new Set(),
  specialistsConsulted: new Map(), // file -> [agents]
  warningsIssued: new Set(), // avoid duplicate warnings
};

function normalizePath(p) {
  return p.replace(/\\/g, "/").toLowerCase();
}

function isExempt(filePath) {
  const normalized = normalizePath(filePath);
  return EXEMPT_PATTERNS.some(pattern => pattern.test(normalized));
}

function getRequiredSpecialists(filePath) {
  const normalized = normalizePath(filePath);
  for (const { pattern, agents, domain } of SPECIALIST_PATTERNS) {
    if (pattern.test(normalized)) {
      return { agents, domain };
    }
  }
  return null;
}

function generateWarning(type, filePath, details) {
  const key = `${type}:${normalizePath(filePath)}`;
  if (sessionState.warningsIssued.has(key)) {
    return null; // Already warned
  }
  sessionState.warningsIssued.add(key);
  
  if (type === "read-first") {
    return `⚠️ **EDIT GUARDIAN**: You're editing \`${filePath}\` without reading it first.

**Action Required:**
1. Read the file to understand current state
2. Then proceed with your edit

This prevents blind edits that break existing functionality.`;
  }
  
  if (type === "specialist") {
    const { agents, domain } = details;
    const agentList = agents.map(a => `\`${a}\``).join(" or ");
    return `⚠️ **EDIT GUARDIAN**: \`${filePath}\` is in the **${domain}** domain.

**Recommended:** Ask ${agentList} agent(s) before modifying.

Use: \`sessions_spawn(agentId="${agents[0]}", task="Review proposed change to ${filePath}: [describe change]")\`

Or proceed if you have domain expertise and understand the implications.`;
  }
  
  return null;
}

const handler = async (event) => {
  if (!event || event.type !== "tool") {
    return;
  }
  
  const { action, params } = event;
  const filePath = params?.file_path || params?.path || "";
  
  if (!filePath) return;
  
  // Track reads
  if (action === "Read") {
    sessionState.filesRead.add(normalizePath(filePath));
    return;
  }
  
  // Track new file creations (Write to non-existent file)
  if (action === "Write") {
    // If file doesn't exist yet, it's a creation - track it
    // We assume if it wasn't read and isn't in filesCreated, it might be new
    // The hook can't check filesystem, so we track writes as potential creates
    if (!sessionState.filesRead.has(normalizePath(filePath))) {
      sessionState.filesCreated.add(normalizePath(filePath));
    }
  }
  
  // Check edits and writes to existing files
  if (action === "Edit" || action === "Write") {
    const normalized = normalizePath(filePath);
    const warnings = [];
    
    // Skip if exempt
    if (isExempt(filePath)) {
      return;
    }
    
    // Skip if file was created this session
    if (sessionState.filesCreated.has(normalized)) {
      return;
    }
    
    // Rule 1: Read before edit
    if (!sessionState.filesRead.has(normalized)) {
      const warning = generateWarning("read-first", filePath);
      if (warning) warnings.push(warning);
    }
    
    // Rule 2: Specialist consultation
    const specialistInfo = getRequiredSpecialists(filePath);
    if (specialistInfo) {
      const consulted = sessionState.specialistsConsulted.get(normalized) || [];
      const unconsulted = specialistInfo.agents.filter(a => !consulted.includes(a));
      
      if (unconsulted.length > 0) {
        const warning = generateWarning("specialist", filePath, {
          agents: unconsulted,
          domain: specialistInfo.domain,
        });
        if (warning) warnings.push(warning);
      }
    }
    
    // Inject warnings as system messages
    if (warnings.length > 0 && event.context) {
      event.context.systemMessages = event.context.systemMessages || [];
      event.context.systemMessages.push({
        role: "system",
        content: warnings.join("\n\n---\n\n"),
        source: "hook:edit-guardian",
      });
      
      console.log(`[edit-guardian] Issued ${warnings.length} warning(s) for ${filePath}`);
    }
  }
};

// Allow external marking of specialist consultation
handler.markConsulted = (filePath, agentId) => {
  const normalized = normalizePath(filePath);
  const existing = sessionState.specialistsConsulted.get(normalized) || [];
  if (!existing.includes(agentId)) {
    existing.push(agentId);
    sessionState.specialistsConsulted.set(normalized, existing);
  }
};

// Allow checking state (for debugging)
handler.getState = () => ({ ...sessionState });

module.exports = handler;
module.exports.default = handler;
