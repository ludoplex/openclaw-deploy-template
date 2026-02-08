/**
 * Hindsight Enforcer Hook
 * Spawns hindsight agent when any agent completes a project.
 * Injects reminder into all agent contexts about post-completion review.
 */

const HINDSIGHT_REMINDER = `
## 🔍 HINDSIGHT ENFORCEMENT (Injected by Hook)

**MANDATORY on project completion:**

When you complete a project (shipped, merged, deployed, "done"), you MUST:

1. Spawn \`hindsight\` agent with:
   - Project directory path
   - Your session ID
   - List of agents involved
   - What was delivered

2. Wait for hindsight to produce its report at:
   \`C:\\Users\\user\\.openclaw\\workspace\\hindsight\\{project}-{date}.md\`

**Completion triggers:**
- "project complete"
- "implementation complete" 
- "deployed"
- "merged"
- "shipped"
- Final commit message

**No exceptions.** Every completion gets reviewed.
`;

const COMPLETION_PATTERNS = [
  /project\s+complete/i,
  /implementation\s+complete/i,
  /task\s+complete/i,
  /finished\s+implementing/i,
  /successfully\s+deployed/i,
  /merged\s+to\s+(main|master)/i,
  /shipped/i,
  /ready\s+for\s+production/i,
];

const handler = async (event) => {
  // Inject reminder on agent bootstrap
  if (event?.type === "agent" && event?.action === "bootstrap") {
    if (event.context?.bootstrapFiles && Array.isArray(event.context.bootstrapFiles)) {
      event.context.bootstrapFiles.push({
        name: "HINDSIGHT_REMINDER.md",
        path: "HINDSIGHT_REMINDER.md",
        content: HINDSIGHT_REMINDER,
        source: "hook:hindsight-enforcer",
      });
      console.log("[hindsight-enforcer] Injected completion review reminder");
    }
  }

  // Detect completion in agent messages
  if (event?.type === "message" && event?.role === "assistant") {
    const content = event.content || "";
    const isCompletion = COMPLETION_PATTERNS.some(pattern => pattern.test(content));
    
    if (isCompletion) {
      console.log("[hindsight-enforcer] 🔍 Completion detected! Hindsight review required.");
      // Flag for hindsight spawn - actual spawn handled by agent reading this flag
      return {
        action: "spawn_required",
        agent: "hindsight",
        reason: "Project completion detected",
        context: {
          sessionId: event.sessionId,
          agentId: event.agentId,
          completionText: content.slice(0, 500),
        }
      };
    }
  }
};

module.exports = handler;
module.exports.default = handler;
