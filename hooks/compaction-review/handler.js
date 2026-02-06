/**
 * Compaction Review Hook
 *
 * Captures conversation turns before compaction to a file, allowing
 * the agent to review the original context after compaction occurs.
 *
 * Since compaction hooks are fire-and-forget (can't inject context),
 * we persist the pre-compaction context to a file that the agent
 * can be instructed to read.
 */

const fs = require('fs');
const path = require('path');

// Where to save pre-compaction context
const REVIEW_FILE = path.join(process.env.USERPROFILE || process.env.HOME, '.openclaw', 'workspace', 'memory', 'compaction-review.md');

// How many recent turns to preserve for review
const TURNS_TO_PRESERVE = 30;

/**
 * Extract the last N user/assistant message pairs from conversation
 */
function extractRecentTurns(messages, count) {
  if (!Array.isArray(messages)) return [];

  const turns = [];
  for (let i = messages.length - 1; i >= 0 && turns.length < count * 2; i--) {
    const msg = messages[i];
    if (!msg || typeof msg !== 'object') continue;

    const role = msg.role;
    if (role === 'user' || role === 'assistant') {
      let content = '';

      if (typeof msg.content === 'string') {
        content = msg.content;
      } else if (Array.isArray(msg.content)) {
        content = msg.content
          .filter(b => b && b.type === 'text' && b.text)
          .map(b => b.text)
          .join('\n');
      }

      if (content.trim()) {
        turns.unshift({ role, content: content.slice(0, 3000) }); // Limit per-message size
      }
    }
  }

  return turns;
}

/**
 * Format turns for markdown display
 */
function formatTurns(turns) {
  return turns.map(t => `### ${t.role === 'user' ? 'User' : 'Assistant'}\n\n${t.content}`).join('\n\n---\n\n');
}

const handler = async (event) => {
  // Before compaction: save recent turns to file
  if (event.type === 'before_compaction') {
    const messages = event.messages || event.data?.messages || [];
    const recentTurns = extractRecentTurns(messages, TURNS_TO_PRESERVE);

    if (recentTurns.length > 0) {
      const timestamp = new Date().toISOString();
      const content = `# Pre-Compaction Context Snapshot

**Captured**: ${timestamp}
**Message Count**: ${messages.length}
**Turns Saved**: ${recentTurns.length}

---

## Last ${recentTurns.length} Messages Before Compaction

${formatTurns(recentTurns)}

---

## Review Instructions

After compaction, please verify:
- [ ] All active tasks are mentioned in the summary
- [ ] File paths and names are accurate
- [ ] User preferences are captured
- [ ] Pending work items are noted
- [ ] No hallucinated or incorrect details

If the summary is missing critical information, please note the discrepancies.
`;

      try {
        // Ensure directory exists
        const dir = path.dirname(REVIEW_FILE);
        if (!fs.existsSync(dir)) {
          fs.mkdirSync(dir, { recursive: true });
        }

        fs.writeFileSync(REVIEW_FILE, content, 'utf-8');
        console.log(`[compaction-review] Saved ${recentTurns.length} turns to ${REVIEW_FILE}`);
      } catch (err) {
        console.error(`[compaction-review] Failed to save context: ${err.message}`);
      }
    }
    return;
  }

  // After compaction: log that compaction occurred
  if (event.type === 'after_compaction') {
    const summary = event.summary || event.data?.summary || '';
    console.log(`[compaction-review] Compaction completed. Summary length: ${summary.length} chars`);
    console.log(`[compaction-review] Pre-compaction context available at: ${REVIEW_FILE}`);

    // Append the summary to the review file for comparison
    if (summary && fs.existsSync(REVIEW_FILE)) {
      try {
        const appendContent = `\n\n---\n\n## Compaction Summary Generated\n\n${summary}\n`;
        fs.appendFileSync(REVIEW_FILE, appendContent, 'utf-8');
        console.log(`[compaction-review] Appended summary to review file`);
      } catch (err) {
        console.error(`[compaction-review] Failed to append summary: ${err.message}`);
      }
    }
    return;
  }
};

// Export for OpenClaw hook system
module.exports = handler;
module.exports.default = handler;
module.exports.events = ['before_compaction', 'after_compaction'];
