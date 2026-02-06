/**
 * Resource Paths Injector Hook
 * Injects file paths to relevant resources into agent bootstrap context.
 * Ensures agents know what files exist so they can READ them.
 */

const fs = require('fs');
const path = require('path');

// File patterns to look for
const RESOURCE_PATTERNS = [
  { pattern: /\.md$/i, category: 'Documentation' },
  { pattern: /^README/i, category: 'Documentation' },
  { pattern: /^AGENTS\.md$/i, category: 'Agent Config', priority: true },
  { pattern: /^SOUL\.md$/i, category: 'Agent Config', priority: true },
  { pattern: /^MEMORY\.md$/i, category: 'Memory', priority: true },
  { pattern: /^BOOT\.md$/i, category: 'Boot', priority: true },
  { pattern: /^\.env/i, category: 'Config' },
  { pattern: /config\.(json|yaml|toml|js|ts)$/i, category: 'Config' },
  { pattern: /package\.json$/i, category: 'Project' },
  { pattern: /Makefile$/i, category: 'Build' },
];

function scanDirectory(dir, maxDepth = 3, currentDepth = 0) {
  const results = [];

  if (currentDepth >= maxDepth) return results;

  try {
    const entries = fs.readdirSync(dir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);

      // Skip hidden directories and common excludes
      if (entry.name.startsWith('.') && entry.isDirectory()) continue;
      if (['node_modules', 'dist', 'build', '.git', '__pycache__'].includes(entry.name)) continue;

      if (entry.isDirectory()) {
        results.push(...scanDirectory(fullPath, maxDepth, currentDepth + 1));
      } else {
        for (const { pattern, category, priority } of RESOURCE_PATTERNS) {
          if (pattern.test(entry.name)) {
            results.push({
              path: fullPath,
              name: entry.name,
              category,
              priority: priority || false,
            });
            break;
          }
        }
      }
    }
  } catch (err) {
    console.log(`[resource-paths-injector] Could not scan ${dir}: ${err.message}`);
  }

  return results;
}

function generateResourceList(resources, workspaceDir) {
  const priorityResources = resources.filter(r => r.priority);
  const otherResources = resources.filter(r => !r.priority);

  const byCategory = {};
  for (const r of otherResources) {
    if (!byCategory[r.category]) byCategory[r.category] = [];
    byCategory[r.category].push(r);
  }

  let content = `## 📂 AVAILABLE RESOURCES (Injected by Hook)

**IMPORTANT**: These files exist in your workspace. READ them before making assumptions.

### Priority Files (READ THESE FIRST)
`;

  if (priorityResources.length > 0) {
    for (const r of priorityResources) {
      const relativePath = path.relative(workspaceDir, r.path).replace(/\\/g, '/');
      content += `- \`${relativePath}\` — ${r.category}\n`;
    }
  } else {
    content += `_None found_\n`;
  }

  content += `\n### By Category\n`;

  for (const [category, files] of Object.entries(byCategory)) {
    content += `\n**${category}:**\n`;
    for (const r of files.slice(0, 10)) { // Limit per category
      const relativePath = path.relative(workspaceDir, r.path).replace(/\\/g, '/');
      content += `- \`${relativePath}\`\n`;
    }
    if (files.length > 10) {
      content += `- _...and ${files.length - 10} more_\n`;
    }
  }

  content += `
### How to Use
1. **READ** any file before editing it
2. **CHECK** if a file exists before creating a new one
3. **CONSULT** documentation files for context

**Rule**: If a resource exists, READ it. Don't assume. Don't recreate.
`;

  return content;
}

const handler = async (event) => {
  if (!event || event.type !== 'agent' || event.action !== 'bootstrap') {
    return;
  }

  // Get workspace directory
  const workspaceDir = event.context?.workspaceDir ||
                       event.data?.workspaceDir ||
                       process.env.OPENCLAW_WORKSPACE ||
                       path.join(process.env.HOME || process.env.USERPROFILE || '', '.openclaw', 'workspace');

  // Scan for resources
  const resources = scanDirectory(workspaceDir);

  // Also scan memory directory specifically
  const memoryDir = path.join(workspaceDir, 'memory');
  if (fs.existsSync(memoryDir)) {
    const memoryFiles = scanDirectory(memoryDir, 1);
    for (const f of memoryFiles) {
      f.category = 'Memory';
      f.priority = f.name.toLowerCase() === 'memory.md';
    }
    resources.push(...memoryFiles);
  }

  if (resources.length === 0) {
    console.log('[resource-paths-injector] No resources found');
    return;
  }

  // Generate the resource list content
  const resourceList = generateResourceList(resources, workspaceDir);

  // Inject into bootstrap files
  if (event.context?.bootstrapFiles && Array.isArray(event.context.bootstrapFiles)) {
    event.context.bootstrapFiles.push({
      name: 'RESOURCES.md',
      path: 'RESOURCES.md',
      content: resourceList,
      source: 'hook:resource-paths-injector',
    });

    console.log(`[resource-paths-injector] Injected ${resources.length} resource paths into bootstrap context`);
  }
};

module.exports = handler;
module.exports.default = handler;
