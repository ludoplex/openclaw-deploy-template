/**
 * Workflow Enforcer Hook
 * Injects workflow routing reminder into agent bootstrap context.
 */

import type { HookHandler } from "openclaw/hooks";

const WORKFLOW_REMINDER = `
## ⚠️ WORKFLOW ENFORCEMENT (Injected by Hook)

**BEFORE starting any task, route it:**

| Task Type | Use This | NOT Claude |
|-----------|----------|------------|
| Simple code gen, boilerplate | Local LLM | ❌ |
| JSON/format/transform | LLM or jq/sed | ❌ |
| Architecture decisions | lmarena.ai (multi-model) | ❌ |
| File search/ops | rg, fd, grep, PowerShell | ❌ |
| Git operations | git, gh CLI | ❌ |
| API testing | curl, Invoke-WebRequest | ❌ |
| Complex reasoning | Claude | ✅ |
| Multi-file refactoring | Claude | ✅ |
| Tool orchestration | Claude | ✅ |

**Quick check:** \`.\scripts\should-use-claude.ps1 "task description"\`

**Rule:** Cheapest tool first. Escalate only when needed.
`;

const handler: HookHandler = async (event) => {
  // Only trigger on agent:bootstrap
  if (event.type !== "agent" || event.action !== "bootstrap") {
    return;
  }

  // Inject workflow reminder into bootstrap files
  if (event.context.bootstrapFiles) {
    event.context.bootstrapFiles.push({
      path: "WORKFLOW_REMINDER.md",
      content: WORKFLOW_REMINDER,
      source: "hook:workflow-enforcer",
    });
    
    console.log("[workflow-enforcer] Injected workflow reminder into bootstrap context");
  }
};

export default handler;
