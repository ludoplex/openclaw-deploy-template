/**
 * Read Before Edit Hook
 * Forces agents to read files before editing them.
 * Tracks reads per session, blocks edits to unread files.
 */

// Track which files have been read per session
const readFiles = new Map(); // sessionKey -> Set<filePath>

function normalizeFilePath(filePath) {
  if (!filePath) return null;
  // Normalize path separators and case for Windows
  return filePath.replace(/\\/g, '/').toLowerCase();
}

function getSessionReads(sessionKey) {
  if (!readFiles.has(sessionKey)) {
    readFiles.set(sessionKey, new Set());
  }
  return readFiles.get(sessionKey);
}

const handler = async (event) => {
  if (event.type !== 'tool') return;

  const toolName = event.data?.toolName || event.data?.tool;
  const args = event.data?.args || event.data?.arguments || {};
  const sessionKey = event.sessionKey || 'default';

  // Track reads
  if (event.action === 'post-execute' && toolName === 'read') {
    const filePath = args.file_path || args.path || args.filePath;
    if (filePath) {
      const normalized = normalizeFilePath(filePath);
      getSessionReads(sessionKey).add(normalized);
      console.log(`[read-before-edit] Tracked read: ${normalized}`);
    }
    return;
  }

  // Block edits to unread files
  if (event.action === 'pre-execute' && (toolName === 'edit' || toolName === 'write')) {
    const filePath = args.file_path || args.path || args.filePath;
    if (!filePath) return;

    const normalized = normalizeFilePath(filePath);
    const sessionReads = getSessionReads(sessionKey);

    if (!sessionReads.has(normalized)) {
      // File hasn't been read - inject warning
      event.messages.push(
        `⚠️ **READ BEFORE EDIT**: You must read "${filePath}" before editing it. ` +
        `Use the read tool first to see the current contents, then retry your edit.`
      );

      // Block the tool execution
      if (event.block) {
        event.block(`File not read: ${filePath}`);
      } else if (event.preventDefault) {
        event.preventDefault();
      }

      console.log(`[read-before-edit] BLOCKED edit to unread file: ${filePath}`);
      return;
    }

    console.log(`[read-before-edit] Allowed edit to previously read file: ${filePath}`);
  }
};

module.exports = handler;
module.exports.default = handler;
