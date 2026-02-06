/**
 * Spawn Roster Hook
 * Injects full agent roster into context so agents know who to spawn/delegate to.
 */

const AGENT_ROSTER = `
## 🤖 Agent Roster (23 Specialists)

Use \`sessions_spawn(agentId="...", task="...")\` to delegate work.

| Agent | Emoji | Specialization |
|-------|-------|----------------|
| main | 🦞 | Personal assistant, general tasks, coordination |
| ops | 📊 | MHI/DSAIC/ComputerStore business ops, Zoho integration |
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
| dev | 💻 | General software development |
| research | 🔬 | Deep research, literature review |
| statanalysis | 📉 | Statistical analysis, anomaly detection |

**Collaboration patterns:**
- Complex strategy → spawn ballistics + analyst + seeker in parallel
- Code projects → spawn dev/webdev/cosmo + testcov + cicd
- Research tasks → spawn seeker + research + analyst

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
