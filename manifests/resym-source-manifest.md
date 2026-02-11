# resym Source Manifest

Generated: 2026-02-11
Source: https://github.com/ludoplex/resym (fork of ergrelet/resym)
Path: `C:\resym`

## Overview

resym is a utility for browsing and extracting C/C++ type declarations from PDB (Program Database) files. Available as native GUI, CLI, and WebAssembly versions.

**Inspiration:** PDBRipper, pdbex

## Key Features

- Cross-platform (native + web)
- GUI (`resym`) and CLI (`resymc`) versions
- C and C++ type reconstruction
- PDB diff generation (compare two PDBs)
- Performant on huge PDB files

## Architecture

```
PDB File → resym_core → Type AST → C/C++ Output
              ↓
         pdb crate (Rust)
```

## Crates

| Crate | Path | Purpose |
|-------|------|---------|
| `resym` | `resym/` | GUI application (native + WASM) |
| `resymc` | `resymc/` | CLI application |
| `resym_core` | `resym_core/` | Core library (PDB parsing, type reconstruction) |

## Key Files

### GUI (`resym/src/`)
| File | Purpose |
|------|---------|
| `main.rs` | Entry point |
| `resym_app.rs` | Main application state |
| `frontend.rs` | UI rendering |
| `settings.rs` | Configuration |
| `syntax_highlighting.rs` | Code highlighting |
| `ui_components/type_list.rs` | Type browser |
| `ui_components/type_search.rs` | Search functionality |
| `ui_components/code_view.rs` | Code display |

### CLI (`resymc/src/`)
| File | Purpose |
|------|---------|
| `main.rs` | CLI entry |
| `frontend.rs` | CLI interface |

## CLI Commands

```bash
# List types in PDB
resymc list <pdb_path>

# Dump single type
resymc dump <pdb_path> <type_name>

# Dump all types
resymc dump-all <pdb_path> [--output <dir>]

# Diff types between two PDBs
resymc diff <pdb1> <pdb2> <type_name>
```

## Output Example

```c
// From Windows kernel PDB
typedef struct _EPROCESS {
    KPROCESS Pcb;
    EX_PUSH_LOCK ProcessLock;
    LARGE_INTEGER CreateTime;
    LARGE_INTEGER ExitTime;
    EX_RUNDOWN_REF RundownProtect;
    PVOID UniqueProcessId;
    LIST_ENTRY ActiveProcessLinks;
    // ...
} EPROCESS, *PEPROCESS;
```

## Web Version

Live at: https://ergrelet.github.io/resym/

Built with WASM (`target_arch = "wasm32"`), uses egui/eframe for UI.

## Dependencies

| Crate | Purpose |
|-------|---------|
| `pdb` | PDB file parsing |
| `egui` / `eframe` | GUI framework |
| `syntect` | Syntax highlighting |

## Integration with Cosmopolitan

**Challenge:** resym is Rust-based; Cosmopolitan targets C.

**Approaches:**
1. **WASM Bridge:** Run resym as WASM module, call from C via WAMR
2. **FFI Export:** Create C-callable Rust library, link statically
3. **Reimplementation:** Port core PDB parsing to C (significant effort)

**Recommended:** Option 1 (WASM) — aligns with apeswarm pattern.

## What Does NOT Exist

- ❌ No DWARF support — PDB only (Windows)
- ❌ No ELF/Mach-O debug info
- ❌ No type inference — extraction only
- ❌ No C API — Rust only
- ❌ No Cosmopolitan build

## Installation

```bash
# From crates.io (when published)
cargo install resym resymc

# From git
cargo install --git https://github.com/ergrelet/resym --tag v0.3.0
```

---

*This manifest is ground truth. Rust codebase, PDB-focused.*
