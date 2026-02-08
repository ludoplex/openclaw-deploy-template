/**
 * Foresight Enforcer Hook
 * Spawns foresight agent when any agent prepares a proposal.
 * Injects reminder into all agent contexts about proposal review.
 */

const FORESIGHT_REMINDER = `
## 🔮 FORESIGHT ENFORCEMENT (Injected by Hook)

**MANDATORY before presenting proposals:**

When you're about to propose an approach, plan, or architecture, you MUST:

1. Spawn \`foresight\` agent with:
   - Full session context
   - Your proposed approach
   - Your agent ID

2. Foresight will read ALL hindsight reports at:
   \`C:\\Users\\user\\.openclaw\\workspace\\hindsight\\*.md\`

3. Wait for foresight review at:
   \`C:\\Users\\user\\.openclaw\\workspace\\foresight\\{proposal}-{date}.md\`

**Proposal triggers:**
- "I propose..."
- "my recommendation is..."
- "the plan is..."
- "here's the approach..."
- "implementation plan:"
- "architecture:"

**Override:** User can say "skip foresight" for trivial proposals.

**No skipping for:** Architecture decisions, new projects, major refactors.
`;

const PROPOSAL_PATTERNS = [
  /I\s+propose/i,
  /my\s+recommendation\s+is/i,
  /the\s+plan\s+is/i,
  /here'?s?\s+the\s+approach/i,
  /implementation\s+plan/i,
  /architecture\s+proposal/i,
  /technical\s+design/i,
  /I\s+suggest\s+we/i,
  /proposed\s+solution/i,
];

const handler = async (event) => {
  // Inject reminder on agent bootstrap
  if (event?.type === "agent" && event?.action === "bootstrap") {
    if (event.context?.bootstrapFiles && Array.isArray(event.context.bootstrapFiles)) {
      event.context.bootstrapFiles.push({
        name: "FORESIGHT_REMINDER.md",
        path: "FORESIGHT_REMINDER.md",
        content: FORESIGHT_REMINDER,
        source: "hook:foresight-enforcer",
      });
      console.log("[foresight-enforcer] Injected proposal review reminder");
    }
  }

  // Detect proposal in agent messages
  if (event?.type === "message" && event?.role === "assistant") {
    const content = event.content || "";
    const isProposal = PROPOSAL_PATTERNS.some(pattern => pattern.test(content));
    
    if (isProposal) {
      console.log("[foresight-enforcer] 🔮 Proposal detected! Foresight review required.");
      // Flag for foresight spawn - actual spawn handled by agent reading this flag
      return {
        action: "spawn_required",
        agent: "foresight",
        reason: "Proposal detected",
        context: {
          sessionId: event.sessionId,
          agentId: event.agentId,
          proposalText: content.slice(0, 1000),
          hindsightPath: "C:\\Users\\user\\.openclaw\\workspace\\hindsight",
        }
      };
    }
  }
};

module.exports = handler;
module.exports.default = handler;
