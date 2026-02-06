/**
 * Check Before Create Hook
 * Forces agents to verify files don't exist before creating them.
 */

const fs = require('fs');
const path = require('path');

function normalizeFilePath(filePath) {
  if (!filePath) return null;
  return filePath.replace(/\\/g, '/');
}

const handler = async (event) => {
  if (event.type !== 'tool' || event.action !== 'pre-execute') return;

  const toolName = event.data?.toolName || event.data?.tool;
  const args = event.data?.args || event.data?.arguments || {};

  // Only intercept write operations
  if (toolName !== 'write') return;

  const filePath = args.file_path || args.path || args.filePath;
  if (!filePath) return;

  const normalized = normalizeFilePath(filePath);

  // Check if file exists
  try {
    if (fs.existsSync(filePath)) {
      // File exists - block creation, tell agent to read first
      event.messages.push(
        `⚠️ **FILE ALREADY EXISTS**: "${filePath}" already exists. ` +
        `You must READ the existing file first before deciding to overwrite it. ` +
        `Use the read tool to see current contents.`
      );

      if (event.block) {
        event.block(`File already exists: ${filePath}`);
      } else if (event.preventDefault) {
        event.preventDefault();
      }

      console.log(`[check-before-create] BLOCKED write to existing file: ${filePath}`);
      return;
    }
  } catch (err) {
    // Can't check existence, allow the operation
    console.log(`[check-before-create] Could not check existence of ${filePath}: ${err.message}`);
  }

  console.log(`[check-before-create] Allowed write to new file: ${filePath}`);
};

module.exports = handler;
module.exports.default = handler;
