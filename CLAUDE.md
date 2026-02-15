# OpenClaw Workspace - Claude Code Instructions

This file provides project-level guidance for Claude Code agents working in the OpenClaw workspace.

## Critical Methodology: Source/Binary Manifest

**Before writing ANY code that uses an external dependency, you MUST have a manifest.**

### The Problem
LLMs hallucinate APIs. They call functions that don't exist, use wrong signatures, and invent features that were never implemented. This wastes time and produces broken code.

### The Solution
Create a **Source Manifest** (or **Binary Manifest** for closed-source) that documents:
1. What functions/classes ACTUALLY exist (with file:line references)
2. What functions you might EXPECT but do NOT exist
3. Correct signatures verified from actual source code

### Workflow

1. **Before using an unfamiliar library:**
   ```
   # Check for existing manifest
   ls manifests/*{library}*-manifest.md

   # If none exists, create one following the pattern
   cat patterns/SOURCE_MANIFEST.md
   ```

2. **Creating a manifest:**
   - Clone or fetch the actual source code (NOT documentation)
   - Enumerate all public interfaces
   - Map each to file:line
   - Document what does NOT exist
   - Save to `manifests/{library}-source-manifest.md`

3. **Using a manifest:**
   - Before calling any API, verify it exists in the manifest
   - Check the signature matches your usage
   - If not in manifest, DO NOT USE - research first

### Key Files

| File | Purpose |
|------|---------|
| `patterns/SOURCE_MANIFEST.md` | Template for source-available deps |
| `patterns/BINARY_MANIFEST.md` | Template for closed binaries |
| `manifests/*-manifest.md` | Per-dependency manifests |

### Existing Manifests

- `manifests/claude-code-source-manifest.md` - Claude Agent SDK Python
- `manifests/openclaw-source-manifest.md` - OpenClaw tools and hooks
- `manifests/cursor-ide-manifest.md` - Cursor IDE binary analysis

## Project Structure

```
~/.openclaw/workspace/
├── CLAUDE.md          # This file
├── SOUL.md            # Agent personality and recovery patterns
├── MEMORY.md          # Lessons learned (REPAIR NOT DELETE)
├── IDENTITY.md        # Agent identity
├── manifests/         # Source/Binary manifests
├── patterns/          # Methodology templates
├── memory/            # Agent memory store
└── ...
```

## Key Principles

### 1. Repair, Not Delete
When encountering corrupted data (transcripts, configs, etc.):
- DO NOT truncate or delete
- DO repair by completing missing data
- Preserve all context

### 2. Verify Before Trusting
- Memory can be outdated
- Documentation can be wrong
- Only source code is truth
- Use manifests as ground truth

### 3. Async Coordination
OpenClaw `sessions_spawn` is non-blocking:
- Returns immediately with `status: "accepted"`
- Announcements arrive asynchronously
- Plan for two-turn patterns when spawning advisors

## Enforcement

The `manifest-enforcer` Claude Code plugin automatically:
- Warns when writing code with unmanifested imports
- Suggests manifests when researching libraries
- Points to existing manifests when available

This is NOT optional. Hallucinated APIs waste time and break code.
