/**
 * Spawn Roster Hook
 * Injects full agent roster into context so agents know who to spawn/delegate to.
 */

const AGENT_ROSTER = `
## 🤖 Agent Roster (26 Specialists)

Use \`sessions_spawn(agentId="...", task="...")\` to delegate work.

### Advisory Triad (spawn for decisions)
| Agent | Emoji | Role |
|-------|-------|------|
| redundant-project-checker | 🔄 | Checks for mature alternatives to proposed tech |
| project-critic | 👹 | Enumerates all failure modes and risks |
| never-say-die | 💪 | Provides solutions to every blocker |

### Temporal Pair (automatic via hooks)
| Agent | Emoji | Trigger |
|-------|-------|---------|
| hindsight | 🔍 | On project completion — reviews what went wrong |
| foresight | 🔮 | On proposal — applies lessons from hindsight archive |

### Specialists
| Agent | Emoji | Specialization |
|-------|-------|----------------|
| main | 🦞 | Orchestrator, user-facing, coordination |
| ops | 📊 | MHI/DSAIC/ComputerStore business ops, Zoho |
| webdev | 🌐 | FastAPI, HTMX, Python web development |
| cosmo | 🌌 | Cosmopolitan/jart, APE binaries, portable C |
| social | 📱 | Mixpost, social media management |
| course | 📚 | Training content, certification curriculum |
| pearsonvue | 🎓 | Testing center operations, exam scheduling |
| ggleap | 🎮 | LAN center management, ggLeap API |
| asm | ⚙️ | AMD64, AArch64, MASM64 assembly |
| metaquest | 🥽 | Meta Quest 3 VR development |
| neteng | 🔌 | Network/systems, AD, deployment |
| roblox | 🧱 | Roblox/Luau game development |
| cicd | 🔄 | GitHub Actions, CI/CD pipelines |
| testcov | 🧪 | Test coverage, pytest, jest, property testing |
| seeker | 🔍 | Advanced search, Fravia methods, OSINT |
| sitecraft | 🏗️ | Domains, hosting, website dev |
| skillsmith | ⚒️ | Agent skills, hooks, token optimization |
| ballistics | 🎯 | GUNDOM SME — ADVISORY ONLY, no direct coding |
| climbibm | 🏔️ | IBM/Climb channel partnership |
| analyst | 📈 | Market analysis, competitive research |
| statanalysis | 📉 | Statistical analysis, anomaly detection |

**Collaboration patterns:**
- Decisions → spawn advisory triad (redundant-project-checker + project-critic + never-say-die)
- Strategy → spawn ballistics + analyst + seeker in parallel
- Code projects → spawn webdev/cosmo + testcov + cicd
- Research → spawn seeker + analyst + statanalysis
- Completions → hindsight auto-spawns (hook enforced)
- Proposals → foresight auto-spawns (hook enforced)

**Rule:** Spawn specialists for focused work. Compile their outputs for user review.
`;

const handler = async (event) => {
  // Trigger on agent bootstrap
  if (!event || event.type !== "agent" || event.action !== "bootstrap") {
    return;
  }

  // Inject roster into bootstrap files
  if (event.context && event.context.bootstrapFiles && Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      name: "AGENT_ROSTER.md",
      path: "AGENT_ROSTER.md", 
      content: AGENT_ROSTER,
      source: "hook:spawn-roster",
    });

    console.log("[spawn-roster] Injected agent roster into bootstrap context");
  }
};

module.exports = handler;
module.exports.default = handler;
