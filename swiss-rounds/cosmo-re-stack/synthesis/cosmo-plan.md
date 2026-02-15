# Cosmo Specialist Work Plan

**Date:** 2026-02-10  
**Agent:** cosmo-specialist  
**Role:** Build infrastructure, Cosmopolitan integration, platform layer

---

## Mission Statement

Own the build infrastructure, APE output, and cosmo-bsd platform integration. You're the glue between "code that works" and "single binary that runs everywhere."

---

## Phase 1: v1.0 — Build Infrastructure

### 1.1 XED Integration for Disassembly

**Task:** Ensure e9studio can use XED from cosmokramerpolitan for x86 disassembly.

**Files to study:**
```
C:\cosmokramerpolitan\third_party\xed\x86ild.greg.c  (42K lines)
C:\cosmokramerpolitan\third_party\xed\x86.h          (11K lines)
C:\cosmokramerpolitan\libc\x86isa.h                  (API surface)
```

**Key APIs:**
```c
int x86ild(struct XedDecodedInst *, const void *, size_t);
const char *GetMnemonic(struct XedDecodedInst *);
```

**Deliverables:**
- [ ] Header shim for e9studio to include XED
- [ ] Build instructions for linking e9studio with XED
- [ ] Verification test: disassemble sample x86-64 binary

**Effort:** 3-5 days

### 1.2 cosmocc Build Pipeline for e9studio

**Task:** Set up build pipeline to produce e9studio as APE binary.

**Reference:** tedit-cosmo's `Makefile.cosmo` pattern

**Files to study:**
```
C:\tedit-cosmo\Makefile.cosmo           (existing pattern)
C:\cosmokramerpolitan\tool\cosmocc\     (toolchain)
C:\cosmokramerpolitan\ape\ape.lds       (linker script)
```

**Build flow:**
```
Source (.c/.cpp)
      │
      ▼
┌─────────────────┐
│    cosmocc      │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│ x86   │ │arm64  │
│ GCC   │ │ GCC   │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         ▼
   ┌───────────┐
   │  apelink  │
   └─────┬─────┘
         ▼
   ┌───────────┐
   │e9studio.com│ (Fat APE)
   └───────────┘
```

**Deliverables:**
- [ ] `Makefile.cosmo` for e9studio
- [ ] Fat APE binary (x86-64 + ARM64)
- [ ] Build verified on Linux, Windows, macOS

**Effort:** 1 week

### 1.3 ZipOS Bundling for Plugins/Resources

**Task:** Bundle e9studio plugins and resources using ZipOS.

**Files to study:**
```
C:\cosmokramerpolitan\libc\runtime\zipos-open.c
C:\cosmokramerpolitan\libc\runtime\zipos-read.c
C:\cosmokramerpolitan\libc\runtime\zipos-mmap.c
```

**Pattern:**
```c
// Access bundled resources via virtual path
FILE *f = fopen("/zip/plugins/default.wasm", "r");
```

**Bundle structure:**
```
cosmo-re-stack.com (APE)
├── /zip/plugins/
│   ├── e9patch.wasm       (core rewriter logic)
│   └── default-config.ini
├── /zip/scripts/
│   └── init.lua           (if Lua scripting enabled)
└── /zip/models/
    └── (optional LLM weights for llamafile mode)
```

**Deliverables:**
- [ ] ZipOS append tool/script for build pipeline
- [ ] e9studio code to read plugins from `/zip/`
- [ ] Verification: plugin loads from embedded ZIP

**Effort:** 3-5 days

### 1.4 APE Self-Modification Support

**Task:** Enable e9studio to modify its own APE (store patched binaries in ZipOS).

**Key APIs (from e9wasm_host.h):**
```c
int e9wasm_zipos_append(const char *name, const uint8_t *data, size_t size);
const char *e9wasm_get_exe_path(void);  // For self-modification
```

**Use case:**
1. User loads binary into e9studio
2. User creates patches
3. Patched binary stored in `/zip/output/patched.exe`
4. APE self-modifies to include the output

**Deliverables:**
- [ ] Self-modification proof-of-concept
- [ ] Safety checks (don't corrupt running APE)
- [ ] Documentation on limitations

**Effort:** 1 week

---

## Phase 2: v1.5 — Quality (Supporting Role)

### 2.1 opentau Build Integration

**Task:** Integrate opentau into the cosmocc build pipeline.

**Dependencies:** opentau repo cloned and analyzed

**Deliverables:**
- [ ] opentau compiles with cosmocc
- [ ] Linked into e9studio as library

**Effort:** 2-3 days

---

## Phase 3: v2.0 — Platform Layer

### 3.1 cosmo-bsd Daemon Build System

**Task:** Build all cosmo-bsd daemons as APE binaries.

**Daemons:**
```
llmd     — LLM inference daemon (llamafile wrapper)
hookd    — Event hook daemon
skilld   — Skill execution daemon
mcpd     — Model Context Protocol daemon
reasond  — Recursive reasoning daemon
agentd   — Inter-agent communication daemon
```

**Each daemon = single APE binary.**

**Deliverables:**
- [ ] Makefile for each daemon
- [ ] All daemons build with cosmocc
- [ ] Daemons communicate via UNIX sockets

**Effort:** 2 weeks

### 3.2 mir JIT Integration for skilld

**Task:** Integrate mir as the JIT compiler for skilld.

**Context:**
- mir compiles C11 directly to machine code
- skilld executes skills in FreeBSD jails
- Jails provide isolation; mir provides speed

**Files to study:**
```
C:\mir\c2mir\c2mir.h          (C → MIR compiler)
C:\mir\mir.h                  (MIR IR)
C:\mir\mir-gen.h              (MIR → native)
```

**Flow:**
```
Skill C code
    │
    ▼
┌─────────┐
│  c2mir  │ (C → MIR IR)
└────┬────┘
     │
     ▼
┌─────────┐
│ mir-gen │ (MIR → native)
└────┬────┘
     │
     ▼
Native code execution (in jail)
```

**Deliverables:**
- [ ] mir compiles with cosmocc
- [ ] skilld can load and JIT compile skills
- [ ] Performance comparison vs WAMR

**Effort:** 3 weeks

### 3.3 Image Build Pipeline

**Task:** Create bootable cosmo-bsd-ai image.

**Target:** Single `.img` file that boots to AI-native OS.

**Components:**
```
cosmo-bsd-ai.img
├── FreeBSD kernel
├── APE userland (busybox-style)
├── /usr/local/sbin/
│   ├── llmd
│   ├── hookd
│   ├── skilld
│   ├── mcpd
│   ├── reasond
│   └── agentd
├── /var/models/
│   └── default.gguf (LLM model)
├── /etc/
│   ├── llmd.conf
│   ├── hookd.d/
│   └── sv/ (runit service dirs)
└── /usr/local/share/skills/
    ├── e9studio/
    └── ludofile/
```

**Deliverables:**
- [ ] Image build script
- [ ] Boot verification (QEMU)
- [ ] Daemon startup via runit/s6

**Effort:** 2 weeks

---

## Key Patterns to Follow

### 1. Sokol Prefix Trick (for multi-platform GUI)

From tedit-cosmo:
```c
// sokol_linux.c
#define sokol_main linux_sokol_main

// sokol_cosmo.c (dispatcher)
int sapp_width(void) {
    if (IsLinux()) return linux_sapp_width();
    if (IsWindows()) return windows_sapp_width();
    if (IsXnu()) return macos_sapp_width();
}
```

Use this pattern for any platform-specific code in e9studio.

### 2. Platform Detection Macros

```c
#include <cosmo.h>

if (IsLinux()) { /* Linux-specific */ }
if (IsWindows()) { /* Windows-specific */ }
if (IsXnu()) { /* macOS-specific */ }
if (IsBsd()) { /* FreeBSD/OpenBSD/NetBSD */ }
```

### 3. ZipOS for Bundling

```c
// Read bundled file
FILE *f = fopen("/zip/config.ini", "r");

// Check if bundled file exists
if (access("/zip/plugins/extra.wasm", F_OK) == 0) {
    // Load optional plugin
}
```

---

## Integration Points with Other Specialists

### With ASM Specialist

| Interface | Direction | Description |
|-----------|-----------|-------------|
| XED headers | Cosmo → ASM | Provide XED API for e9studio disassembly |
| cosmocc flags | Cosmo → ASM | Build flags for e9studio compilation |
| WASM output | ASM → Cosmo | Compiled patches for ZipOS bundling |

### With Seeker Specialist

| Interface | Direction | Description |
|-----------|-----------|-------------|
| ZipOS API | Cosmo → Seeker | How to bundle and read resources |
| Plugin format | Cosmo → Seeker | Spec for e9studio plugins |
| llamafile path | Seeker → Cosmo | Where llamafile expects resources |

---

## Token Budget

| Task | Complexity | Est. Tokens |
|------|------------|-------------|
| XED integration | Medium | 30K-50K |
| cosmocc build pipeline | Medium | 40K-60K |
| ZipOS bundling | Low | 20K-30K |
| APE self-modification | High | 50K-80K |
| opentau build integration | Low | 15K-25K |
| cosmo-bsd daemon builds | High | 80K-120K |
| mir integration | High | 100K-150K |
| Image build pipeline | Medium | 50K-80K |
| **Total** | | **~385K-595K** |

---

## Success Metrics

### v1.0
- [ ] e9studio.com builds as single APE
- [ ] Runs on Linux, Windows, macOS without modification
- [ ] Plugins load from embedded ZipOS

### v1.5
- [ ] opentau integrated into build

### v2.0
- [ ] All 6 daemons build as APE binaries
- [ ] cosmo-bsd-ai.img boots in QEMU
- [ ] llmd serves inference, skilld executes e9studio skill

---

## Immediate Next Steps (Week 1)

1. **Day 1-2:** Study tedit-cosmo's Makefile.cosmo pattern
2. **Day 3-4:** Create e9studio Makefile.cosmo skeleton
3. **Day 5:** XED header shim prototype
4. **Week 1 deliverable:** e9studio compiles with cosmocc (even if incomplete)

---

*"All built with cosmokramerpolitan — one toolchain, seven operating systems, zero dependencies."*
