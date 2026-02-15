# Seeker Specialist Work Plan

**Date:** 2026-02-10  
**Agent:** seeker-specialist  
**Role:** Research, integration, API discovery, glue layer, LLM integration

---

## Mission Statement

Own the integration layer between components. You're the glue expert: discovering APIs, designing interfaces, connecting tedit-cosmo to e9studio, and making llamafile useful for RE tasks.

---

## Phase 1: v1.0 — Integration Layer

### 1.1 tedit-cosmo ↔ e9studio Glue Layer

**Priority:** CRITICAL — Foundation for everything else

**Task:** Create the integration layer that connects tedit-cosmo's UI to e9studio's analysis engine.

**Current state (from Round 1):**
- tedit-cosmo has `disasm_view.h` ready for binary analysis
- e9studio has comprehensive analysis APIs (`e9analysis.h`, `e9decompile.h`)
- **Missing:** No existing bridge between them

**tedit-cosmo integration points:**
```c
// disasm_view.h - already designed for extension
DisasmView *disasm_view_create(Editor *editor);
size_t disasm_view_section_count(DisasmView *view);
const DisasmSymbol *disasm_view_symbol_at(DisasmView *view, uint64_t address);
```

**e9studio APIs to expose:**
```c
// Binary loading and analysis
E9Binary *e9_binary_open(const char *path);
int e9_binary_analyze(E9Binary *bin);

// Function discovery
size_t e9_functions_count(E9Binary *bin);
E9Function *e9_function_at(E9Binary *bin, uint64_t addr);

// Decompilation
char *e9_decompile_function_full(E9Decompile *dc, E9Function *func);

// CFG for visualization
E9CFG *e9_cfg_build(E9Binary *bin, E9Function *func);
int e9_cfg_to_dot(E9CFG *cfg, const char *path);
```

**Glue layer design:**
```c
// glue/e9_tedit_bridge.h

typedef struct {
    E9Binary *binary;
    E9Decompile *decompiler;
    DisasmView *disasm_view;
} E9TeditContext;

// Initialize bridge
E9TeditContext *e9_tedit_init(Editor *editor, const char *binary_path);

// Sync tedit view with e9 analysis
int e9_tedit_sync_disasm(E9TeditContext *ctx);

// Get decompiled C for function under cursor
char *e9_tedit_decompile_at_cursor(E9TeditContext *ctx);

// Navigate to address (bidirectional sync)
int e9_tedit_goto_address(E9TeditContext *ctx, uint64_t addr);
int e9_tedit_goto_function(E9TeditContext *ctx, const char *name);
```

**UI integration (tedit-cosmo side):**
```c
// New menu items in tedit
Menu: File → Open Binary (triggers e9_tedit_init)
Menu: Analysis → Analyze (triggers e9_binary_analyze)
Menu: View → Decompile (triggers e9_tedit_decompile_at_cursor)

// New panes
- Disassembly pane (left): instruction listing
- Decompiler pane (right): C output
- Functions list (sidebar): clickable function navigator
```

**Deliverables:**
- [ ] `e9_tedit_bridge.h` — glue layer header
- [ ] `e9_tedit_bridge.c` — implementation
- [ ] tedit-cosmo UI changes (menus, panes)
- [ ] Demo: open ELF, see disasm + decompiled C side-by-side

**Effort:** 2-3 weeks

### 1.2 llamafile API Integration

**Task:** Connect llamafile's OpenAI-compatible API to e9studio for LLM-assisted analysis.

**llamafile endpoint:**
```
POST http://localhost:8080/v1/chat/completions
{
  "model": "local",
  "messages": [
    {"role": "system", "content": "You are a reverse engineering assistant."},
    {"role": "user", "content": "Explain this function:\n\n```c\n{decompiled_code}\n```"}
  ]
}
```

**Use cases:**
1. **Function explanation:** "What does this function do?"
2. **Variable naming:** "Suggest better names for these variables"
3. **Vulnerability analysis:** "Are there security issues in this code?"
4. **Pattern recognition:** "Is this a known algorithm?"

**Integration design:**
```c
// llm/e9_llm_assist.h

typedef struct {
    char *endpoint;     // "http://localhost:8080/v1/chat/completions"
    int timeout_ms;
    bool available;
} E9LLMConfig;

// Check if llamafile is running
bool e9_llm_available(E9LLMConfig *cfg);

// Get explanation for decompiled function
char *e9_llm_explain_function(E9LLMConfig *cfg, const char *decompiled_c);

// Get variable name suggestions
char *e9_llm_suggest_names(E9LLMConfig *cfg, const char *decompiled_c);

// Get vulnerability analysis
char *e9_llm_analyze_vulns(E9LLMConfig *cfg, const char *decompiled_c);
```

**UI integration:**
```
Context menu on function:
  → "Ask LLM: What does this do?"
  → "Ask LLM: Suggest variable names"
  → "Ask LLM: Find vulnerabilities"
```

**Deliverables:**
- [ ] `e9_llm_assist.h` — LLM integration header
- [ ] HTTP client for llamafile API
- [ ] Prompt templates for RE tasks
- [ ] tedit-cosmo context menu integration
- [ ] Graceful fallback if llamafile not running

**Effort:** 1 week

### 1.3 ludofile Format Detection Frontend

**Task:** Integrate ludofile's polyfile signatures for format detection.

**Current state:**
- e9studio handles ELF, PE, Mach-O, APE
- ludofile has 10,000+ format signatures

**Use case:** User opens unknown binary blob. ludofile identifies:
- Firmware format (various)
- Game ROM format
- Encrypted container
- Embedded data format

**Integration design:**
```c
// format/e9_format_detect.h

typedef struct {
    char *format_name;      // "Nintendo 3DS NCCH"
    char *description;      // "Encrypted game cartridge format"
    uint64_t offset;        // Where format starts in file
    size_t size;           // Format size
    bool extractable;       // Can we extract contents?
} E9FormatMatch;

// Detect format using ludofile
E9FormatMatch *e9_format_detect(const uint8_t *data, size_t size, size_t *count);

// Extract contents if container format
uint8_t *e9_format_extract(const uint8_t *data, size_t size, 
                           E9FormatMatch *match, size_t *out_size);
```

**Flow:**
```
User opens file
    │
    ▼
e9_format_detect() → ludofile signatures
    │
    ├─→ Standard executable? → e9_binary_open()
    │
    └─→ Exotic format? → Show format info, offer extraction
```

**Deliverables:**
- [ ] ludofile C API wrapper
- [ ] Format detection in e9studio
- [ ] UI: show detected format before analysis
- [ ] Extraction support for container formats

**Effort:** 1 week

### 1.4 IDE Protocol Implementation

**Task:** Implement e9studio's IDE protocol for external tool integration.

**From seeker report — existing protocol spec:**
```c
// e9ide_protocol.h
#define E9IDE_METHOD_GET_DECOMPILE   "analysis/getDecompilation"
#define E9IDE_METHOD_PATCH_APPLY     "patch/apply"
#define E9IDE_METHOD_PATCH_SAVE      "patch/save"

// Capabilities
E9IDE_CAP_DECOMPILATION     = 0x0002
E9IDE_CAP_PATCHING          = 0x0008
E9IDE_CAP_LIVE_EDIT         = 0x0020
E9IDE_CAP_WASM_PLUGINS      = 0x0080
E9IDE_CAP_APE               = 0x2000
```

**Why this matters:**
- VSCode extension could use this protocol
- Other editors could integrate
- Automation/scripting tools

**Deliverables:**
- [ ] JSON-RPC server implementation
- [ ] All methods from e9ide_protocol.h
- [ ] Documentation for external integrators
- [ ] Test client (curl scripts or simple tool)

**Effort:** 1-2 weeks

---

## Phase 2: v1.5 — Quality Integration

### 2.1 opentau ↔ llamafile Pipeline

**Task:** Combine opentau's type inference with LLM refinement.

**Pipeline:**
```
Decompiled C (size-based types)
    │
    ▼
opentau (structured type inference)
    │
    ▼
Decompiled C (semantic types, some unknowns)
    │
    ▼
llamafile (LLM refinement of remaining unknowns)
    │
    ▼
Final C (human-readable types)
```

**Why both?**
- opentau: deterministic, structured, fast
- llamafile: handles ambiguous cases, naming

**Deliverables:**
- [ ] Pipeline orchestration
- [ ] Confidence scores for inferred types
- [ ] LLM fallback for low-confidence types

**Effort:** 1 week

---

## Phase 3: v2.0 — Platform Integration

### 3.1 MCP Protocol Integration

**Task:** Implement Model Context Protocol for cosmo-bsd mcpd daemon.

**From daemon architecture:**
```
mcpd — Model Context Protocol daemon
  ├── connects to llmd (for tool-call responses)
  ├── connects to skilld (for tool execution)
  └── handles tool call → execute → result → LLM loop
```

**e9studio as MCP tool:**
```json
{
  "tool": "e9studio",
  "methods": [
    {
      "name": "analyze_binary",
      "params": {"path": "string"},
      "returns": {"functions": "array", "format": "string"}
    },
    {
      "name": "decompile_function",
      "params": {"binary": "string", "function": "string"},
      "returns": {"code": "string"}
    },
    {
      "name": "apply_patch",
      "params": {"binary": "string", "patch": "object"},
      "returns": {"success": "boolean"}
    }
  ]
}
```

**Deliverables:**
- [ ] MCP tool definition for e9studio
- [ ] mcpd client library
- [ ] Integration test with mock mcpd

**Effort:** 2 weeks

### 3.2 hookd Integration

**Task:** Fire hooks from e9studio for event-driven analysis.

**Hook examples:**
- Binary opened → hook to log/track
- Vulnerability found → hook to alert
- Patch applied → hook to verify

**Deliverables:**
- [ ] Hook client for e9studio
- [ ] Hook definitions for RE events
- [ ] Example: vuln-found → reasond → explain

**Effort:** 1 week

---

## API Discovery Checklist

### e9studio APIs (documented in Round 1)

| API | File | Status |
|-----|------|--------|
| `e9_binary_create/open/free` | e9analysis.h | ✅ Documented |
| `e9_binary_analyze` | e9analysis.h | ✅ Documented |
| `e9_cfg_build/free/to_dot` | e9analysis.h | ✅ Documented |
| `e9_decompile_*` | e9decompile.h | ✅ Documented |
| `e9_binpatch_*` | e9binpatch.h | ✅ Documented |
| `e9wasm_*` | e9wasm_host.h | ✅ Documented |
| `e9_ape_parse/extract_*` | e9polyglot.h | ✅ Documented |
| `e9ide_*` | e9ide_protocol.h | ✅ Documented |

### tedit-cosmo APIs

| API | File | Status |
|-----|------|--------|
| `disasm_view_create` | disasm_view.h | ✅ Documented |
| `disasm_view_section_count` | disasm_view.h | ✅ Documented |
| `disasm_view_symbol_at` | disasm_view.h | ✅ Documented |
| `editor_*` | editor.h | Need to verify |
| `buffer_*` | buffer.h | Need to verify |

### llamafile APIs

| API | Endpoint | Status |
|-----|----------|--------|
| Chat completions | POST /v1/chat/completions | ✅ OpenAI-compatible |
| Embeddings | POST /v1/embeddings | ✅ OpenAI-compatible |
| Models | GET /v1/models | ✅ OpenAI-compatible |

### ludofile APIs

| API | Status |
|-----|--------|
| Format detection | Need to discover |
| Signature database | Need to discover |
| Extraction | Need to discover |

---

## Integration Points

### With ASM Specialist

| Interface | Direction | Description |
|-----------|-----------|-------------|
| Glue layer | Seeker + ASM | Joint design of e9_tedit_bridge |
| API usage | ASM → Seeker | Which e9studio APIs to wrap |
| Error handling | ASM → Seeker | What errors to surface to UI |

### With Cosmo Specialist

| Interface | Direction | Description |
|-----------|-----------|-------------|
| ZipOS | Cosmo → Seeker | How to bundle LLM prompts |
| Build integration | Cosmo → Seeker | Linking glue layer into APE |
| Platform detection | Cosmo → Seeker | IsLinux()/IsWindows() for UI |

---

## Token Budget

| Task | Complexity | Est. Tokens |
|------|------------|-------------|
| Glue layer design | High | 80K-120K |
| Glue layer impl | High | 100K-150K |
| llamafile integration | Medium | 30K-50K |
| ludofile integration | Medium | 30K-50K |
| IDE protocol | Medium | 50K-80K |
| opentau+LLM pipeline | Medium | 40K-60K |
| MCP integration | Medium | 60K-100K |
| hookd integration | Low | 20K-30K |
| **Total** | | **~410K-640K** |

---

## Success Metrics

### v1.0
- [ ] Open binary in tedit-cosmo → see disasm + decompiled C
- [ ] Navigate: click function → see decompilation
- [ ] "Ask LLM" context menu works (when llamafile running)
- [ ] Unknown formats identified by ludofile

### v1.5
- [ ] Type inference pipeline produces readable C
- [ ] LLM refines ambiguous types

### v2.0
- [ ] e9studio responds to MCP tool calls
- [ ] RE events fire hooks to hookd

---

## Immediate Next Steps (Week 1)

1. **Day 1-2:** Study tedit-cosmo's disasm_view.h in detail
2. **Day 3-4:** Draft e9_tedit_bridge.h header (coordinate with ASM)
3. **Day 5:** Prototype: tedit-cosmo loads e9studio as library
4. **Week 1 deliverable:** Header file agreed, basic loading works

---

## Prompt Templates (for llamafile)

### Function Explanation
```
You are a reverse engineering assistant. Analyze this decompiled C function and explain:
1. What it does (high-level purpose)
2. Key operations (algorithms, data structures)
3. Potential security concerns

```c
{decompiled_code}
```

Be concise. Focus on actionable insights.
```

### Variable Naming
```
You are a reverse engineering assistant. This is decompiled C with generic variable names.
Suggest meaningful names based on usage patterns.

```c
{decompiled_code}
```

Output format:
- arg0 → suggested_name (reason)
- local8 → suggested_name (reason)
```

### Vulnerability Analysis
```
You are a security researcher. Analyze this decompiled C for vulnerabilities:
- Buffer overflows
- Integer overflows
- Format string bugs
- Use-after-free
- Command injection

```c
{decompiled_code}
```

Rate each finding: Critical / High / Medium / Low
```

---

*"The best integration is invisible — users just see a unified tool."*
