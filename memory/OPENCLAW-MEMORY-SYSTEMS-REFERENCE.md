# OpenClaw Memory Systems Reference

**CRITICAL**: This document describes THREE DISTINCT SYSTEMS that must NEVER be conflated.

---

## System 1: OpenAI Embeddings (API Mechanism)

### What It Is
A remote API service that converts text into numerical vectors (arrays of floats). This is a **mechanism**, not a system with its own storage or logic.

### What It Does
- Accepts text input
- Returns a vector (array of 1536 floats for text-embedding-3-small)
- Used BY other systems (Memory Search) to enable semantic similarity

### What It Does NOT Do
- Does not store anything
- Does not index anything
- Does not search anything
- Has no knowledge of OpenClaw, files, or sessions

### Configuration Location
```
C:\Users\user\.openclaw\openclaw.json
```
Path: `agents.defaults.memorySearch.provider` and `agents.defaults.memorySearch.model`

### Current Config
```json
"provider": "openai",
"model": "text-embedding-3-small",
"remote": {
  "apiKey": "sk-svcacct-...",
  "batch": { "enabled": true, "concurrency": 2 }
}
```

### Documentation
- OpenAI Embeddings API: https://platform.openai.com/docs/guides/embeddings
- OpenAI Batch API: https://platform.openai.com/docs/api-reference/batch
- OpenClaw Memory Docs (embeddings section): `C:\Users\user\openclaw\openclaw-2026.2.2\docs\concepts\memory.md` (lines 78-100, 241-340)

### Source Code
- Embeddings provider: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\embeddings.ts`
- OpenAI embeddings: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\embeddings-openai.ts`
- Batch processing: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\batch-openai.ts`

---

## System 2: Memory Search (Vector Index + Tools)

### What It Is
An indexing and retrieval system that creates a searchable vector database from Markdown files. Provides tools (`memory_search`, `memory_get`) for the agent to query.

### What It Does
- Scans directories for `.md` files ONLY
- Chunks markdown into ~400 token segments with 80 token overlap
- Calls System 1 (Embeddings) to vectorize each chunk
- Stores vectors + metadata in SQLite database
- Provides `memory_search` tool for semantic queries
- Provides `memory_get` tool to read specific files
- Supports hybrid search (BM25 keyword + vector similarity)

### What It Indexes
1. `MEMORY.md` in workspace root
2. `memory/*.md` in workspace
3. All `.md` files in `extraPaths` directories (recursively)

### What It Does NOT Do
- Does NOT index non-markdown files
- Does NOT automatically inject results into context (agent must call tools)
- Does NOT index session transcripts (that's System 3)

### Storage Location
```
C:\Users\user\.openclaw\memory\main.sqlite
```

### Configuration Location
```
C:\Users\user\.openclaw\openclaw.json
```
Path: `agents.defaults.memorySearch`

### Key Config Fields
- `enabled`: boolean
- `extraPaths`: array of directories to scan for .md files
- `sources`: ["memory"] for this system alone
- `chunking.tokens`: chunk size (default 400)
- `chunking.overlap`: overlap between chunks (default 80)
- `query.maxResults`: max results returned
- `query.minScore`: minimum similarity threshold
- `query.hybrid`: BM25 + vector mixing settings
- `cache`: embedding cache settings
- `sync`: when to trigger reindexing

### Current extraPaths (48 directories)
See `C:\Users\user\.openclaw\openclaw.json` lines 40-89

### Documentation
- Main docs: `C:\Users\user\openclaw\openclaw-2026.2.2\docs\concepts\memory.md` (lines 78-420)
- CLI docs: `C:\Users\user\openclaw\openclaw-2026.2.2\docs\cli\memory.md`
- Research notes: `C:\Users\user\openclaw\openclaw-2026.2.2\docs\experiments\research\memory.md`

### Source Code
- Manager: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\manager.ts`
- File listing: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\internal.ts`
- Sync logic: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\sync-memory-files.ts`
- Search logic: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\manager-search.ts`
- Hybrid search: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\hybrid.ts`
- Memory tools: `C:\Users\user\openclaw\openclaw-2026.1.30\src\agents\tools\memory-tool.ts`

---

## System 3: Experimental Session Memory

### What It Is
An EXPERIMENTAL opt-in feature that extends System 2 (Memory Search) to ALSO index session transcript JSONL files. Completely separate indexing path from markdown files.

### What It Does
- Monitors `~/.openclaw/agents/<agentId>/sessions/*.jsonl` files
- Indexes conversation transcripts (user/assistant messages)
- Surfaces results through the same `memory_search` tool
- Uses delta thresholds to trigger async background indexing

### What It Does NOT Do
- Does NOT use `extraPaths` (reads from fixed session directory)
- Does NOT index markdown files (that's System 2)
- Does NOT auto-inject into context (still tool-based)
- Does NOT replace or modify session files

### Session Files Location
```
C:\Users\user\.openclaw\agents\main\sessions\*.jsonl
C:\Users\user\.openclaw\agents\<agentId>\sessions\*.jsonl
```

### Configuration Location
```
C:\Users\user\.openclaw\openclaw.json
```
Path: `agents.defaults.memorySearch.experimental.sessionMemory` and `agents.defaults.memorySearch.sources`

### Key Config Fields
- `experimental.sessionMemory`: boolean (must be true)
- `sources`: must include "sessions" (e.g., ["memory", "sessions"])
- `sync.sessions.deltaBytes`: bytes threshold before reindex (default 100000)
- `sync.sessions.deltaMessages`: message count threshold (default 50)

### Current Config
```json
"experimental": { "sessionMemory": true },
"sources": ["memory", "sessions"]
```

### Documentation
- Main docs: `C:\Users\user\openclaw\openclaw-2026.2.2\docs\concepts\memory.md` (lines 441-481)

### Source Code
- Session sync: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\manager.ts` (search for `syncSessionFiles`, `listSessionFiles`, `shouldSyncSessions`)
- Session listener: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\manager.ts` (search for `ensureSessionListener`)

---

## How The Three Systems Interact

```
┌─────────────────────────────────────────────────────────────────┐
│                        Agent Runtime                            │
│                                                                 │
│  Calls memory_search("query") ──────────────────────────────►  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              SYSTEM 2: Memory Search                            │
│                                                                 │
│  1. Vectorize query using SYSTEM 1 (Embeddings)                │
│  2. Search SQLite for similar vectors                          │
│  3. If sources=["memory","sessions"]:                          │
│     - Search markdown chunks (source="memory")                 │
│     - Search session chunks (source="sessions") ◄─ SYSTEM 3   │
│  4. Merge + rank results                                       │
│  5. Return snippets with file paths + line numbers             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              SYSTEM 1: OpenAI Embeddings                        │
│                                                                 │
│  - Called to vectorize query text                              │
│  - Called during indexing to vectorize chunks                  │
│  - Pure API mechanism, no storage                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Relationship Summary

| Aspect | System 1: Embeddings | System 2: Memory Search | System 3: Session Memory |
|--------|---------------------|------------------------|-------------------------|
| Type | API mechanism | Indexing system | Experimental extension |
| Storage | None | main.sqlite | Same main.sqlite |
| Indexes | Nothing | .md files | .jsonl transcripts |
| Source dirs | N/A | workspace + extraPaths | agents/*/sessions/ |
| Tools | None | memory_search, memory_get | Same tools |
| Required | Yes (by System 2) | Optional | Optional |
| Config key | provider, model | memorySearch.* | experimental.sessionMemory |

---

## NEVER Conflate These Systems

- Embeddings are NOT indexing
- Memory Search is NOT RAG (no auto-injection)
- Session Memory is NOT the session-memory hook (different thing)
- extraPaths affects ONLY System 2 markdown indexing
- Session transcripts are indexed by System 3, NOT extraPaths

---

## Current Optimization Status

Last updated: 2026-02-12

### System 1 (Embeddings)
- Provider: OpenAI
- Model: text-embedding-3-small
- Batch mode: enabled, concurrency 2

### System 2 (Memory Search)
- extraPaths: 48 directories (reduced from 60, removed 3rd party docs)
- Chunking: 1024 tokens, 128 overlap
- Query: maxResults 6, minScore 0.4
- Hybrid: enabled, vectorWeight 0.7, textWeight 0.3
- Cache: enabled, maxEntries 100000

### System 3 (Session Memory)
- Enabled: true
- Sources: ["memory", "sessions"]
- Delta thresholds: 100000 bytes, 50 messages

---

## File Paths Quick Reference

### Configuration
- Main config: `C:\Users\user\.openclaw\openclaw.json`

### Storage
- Vector index: `C:\Users\user\.openclaw\memory\main.sqlite`
- Session transcripts: `C:\Users\user\.openclaw\agents\main\sessions\*.jsonl`
- Workspace memory: `C:\Users\user\.openclaw\workspace\memory\*.md`

### Documentation
- Memory concepts: `C:\Users\user\openclaw\openclaw-2026.2.2\docs\concepts\memory.md`
- Memory CLI: `C:\Users\user\openclaw\openclaw-2026.2.2\docs\cli\memory.md`
- Memory research: `C:\Users\user\openclaw\openclaw-2026.2.2\docs\experiments\research\memory.md`
- Gateway config: `C:\Users\user\openclaw\openclaw-2026.2.2\docs\gateway\configuration.md`

### Source Code
- Memory manager: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\manager.ts`
- Internal utils: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\internal.ts`
- Embeddings: `C:\Users\user\openclaw\openclaw-2026.1.30\src\memory\embeddings.ts`
- Memory tools: `C:\Users\user\openclaw\openclaw-2026.1.30\src\agents\tools\memory-tool.ts`
