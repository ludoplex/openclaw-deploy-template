/**
 * Agent Communications Hook
 * Injects inter-agent messaging protocol into all agent contexts.
 */

const AGENT_COMMS_PROTOCOL = `
## 📡 Inter-Agent Direct Communication

Agents can message each other directly without going through main.

### How to Message Another Agent

\`\`\`
agent_message(
  to="agent-id",
  message="your message here",
  priority="normal|urgent|fyi"
)
\`\`\`

### Priority Levels
- **urgent**: Blocks sender until recipient responds (use sparingly)
- **normal**: Queued for recipient's next turn (default)
- **fyi**: Fire-and-forget, no response expected

### Communication Patterns

**1. Advisory Triad Coordination**
When spawned together, the triad should:
- project-critic broadcasts concerns to redundant-project-checker and never-say-die
- never-say-die responds to each concern with solutions
- redundant-project-checker adds alternatives where relevant
- All three compile into unified response for main

\`\`\`
// project-critic to peers
agent_message(to="never-say-die", message="Concern: No fallback if API fails", priority="normal")
agent_message(to="redundant-project-checker", message="Proposed: Custom auth system", priority="normal")
\`\`\`

**2. Hindsight/Foresight Loop**
- foresight queries hindsight archive directly (file read)
- For clarification, foresight can message hindsight:
\`\`\`
agent_message(to="hindsight", message="Clarify: What caused the auth failure in project X?", priority="normal")
\`\`\`

**3. Specialist Handoffs**
When a specialist needs another specialist:
\`\`\`
// webdev to testcov
agent_message(to="testcov", message="Ready for test coverage review: /path/to/module", priority="normal")

// cosmo to asm
agent_message(to="asm", message="Need optimized memcpy for ARM64, current impl at line 45", priority="normal")
\`\`\`

**4. Escalation to Main**
Any agent can escalate to main:
\`\`\`
agent_message(to="main", message="BLOCKER: User decision required on X vs Y", priority="urgent")
\`\`\`

### Broadcast Messages

Message multiple agents:
\`\`\`
agent_broadcast(
  to=["project-critic", "redundant-project-checker", "never-say-die"],
  message="Context: User wants to build X with Y",
  priority="normal"
)
\`\`\`

### Message Inbox

Check for incoming messages:
\`\`\`
messages = agent_inbox()
// Returns: [{from: "agent-id", message: "...", priority: "...", timestamp: "..."}]
\`\`\`

### Rules
1. **Don't spam** — consolidate related points into one message
2. **Be specific** — include file paths, line numbers, context
3. **Tag priority correctly** — urgent means BLOCKING
4. **Respond promptly** — don't leave urgent messages hanging
5. **CC main on escalations** — main should know about blockers
`;

const handler = async (event) => {
  if (!event || event.type !== "agent" || event.action !== "bootstrap") {
    return;
  }

  if (event.context?.bootstrapFiles && Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      name: "AGENT_COMMS.md",
      path: "AGENT_COMMS.md",
      content: AGENT_COMMS_PROTOCOL,
      source: "hook:agent-comms",
    });

    console.log("[agent-comms] Injected inter-agent communication protocol");
  }
};

module.exports = handler;
module.exports.default = handler;
