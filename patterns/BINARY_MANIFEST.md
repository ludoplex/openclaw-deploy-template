# Binary Manifest Methodology

**Purpose:** Achieve source-manifest-equivalent understanding when only binaries are available. Prevent hallucinating interfaces, calling nonexistent functions, or misunderstanding binary behavior.

## When to Apply

- Proprietary libraries without headers
- Legacy binaries being wrapped or extended
- Security analysis of third-party components
- Before writing code that must interop with closed binaries
- When source is unavailable (use SOURCE_MANIFEST.md when it is)

## Tools Required

| Tool | Purpose |
|------|---------|
| `nm` | Symbol extraction |
| `objdump` | Disassembly, relocations |
| `readelf` | ELF structure, sections |
| `strings` | Embedded string literals |
| `e9studio` | CFG generation, analysis |
| `e9patch` | Symbol injection, instrumentation |
| `Ghidra/IDA` | Decompilation (optional) |

## Process

### 1. Extract Symbols
```bash
# ELF
nm -C binary > symbols.txt
readelf -s binary >> symbols.txt
objdump -t binary >> symbols.txt

# PE (Windows)
dumpbin /exports binary.dll
dumpbin /symbols binary.exe
```

### 2. Generate Control Flow Graphs
```bash
# Using e9studio
e9studio --cfg binary -o cfg/

# Output: DOT files per function
```

### 3. Identify Entry Points

Extract and document:
- `main` / `WinMain` / `DllMain`
- Exported functions (shared libraries)
- `.init` / `.fini` / `.init_array` / `.fini_array`
- Signal handlers
- Vtables (C++)
- Interrupt vectors (embedded)

### 4. Map Calling Conventions

For each function:
| Field | Description |
|-------|-------------|
| Address | Virtual address |
| File Offset | Offset in binary |
| Name | Symbol or analyst-assigned |
| Convention | cdecl/stdcall/fastcall/sysv |
| Parameters | Count, types if recoverable |
| Return | Type if recoverable |
| Stack Frame | Size, locals layout |

### 5. Enumerate Strings
```bash
strings -a -t x binary > strings.txt
```

Cross-reference strings to loading functions.

### 6. Trace External Dependencies
```bash
# ELF
ldd binary
readelf -d binary | grep NEEDED
objdump -T binary  # Dynamic symbols

# PE
dumpbin /dependents binary.exe
```

Document every syscall and library call.

### 7. Document What is NOT Present

Explicitly list:
- No network calls (if absent)
- No file I/O (if absent)
- No threading primitives
- Missing expected functionality
- Stripped symbols that couldn't be recovered

### 8. Inject Recovered Symbols (Optional)
```bash
# Using e9patch to add symbol table
e9patch -M 'addr == 0x401230' -P 'sym("parse_config")' binary -o binary.sym
```

Result: Debuggable binary with recovered names.

## Output Files

| File | Contents |
|------|----------|
| `{binary}-symbol-map.md` | Address-to-name mapping |
| `{binary}-cfg/` | Directory of DOT files |
| `{binary}-imports.md` | External dependencies |
| `{binary}-strings.md` | String table with xrefs |
| `{binary}-manifest.md` | Unified reference |

## Manifest Format

```markdown
# {Binary} Binary Manifest

Generated: {date}
Binary: {path}
SHA256: {hash}
Format: ELF64 / PE32+ / Mach-O

## Recovered Functions

### 0x00401230 | parse_config
- **File offset:** 0x1230
- **Signature:** `(char*, int) -> int` (deduced)
- **Calls:** fopen, fread, malloc, strcmp
- **Called by:** main, reload_handler
- **Strings:** "config.ini", "error: %s"
- **CFG nodes:** 47

## Imports

| Library | Function | Used By |
|---------|----------|---------|
| libc.so.6 | fopen | 0x401230, 0x401890 |

## What Does NOT Exist

- ❌ No network syscalls (socket, connect, send, recv)
- ❌ No threading (pthread_*, CreateThread)
- ❌ Symbol `init_network` — does not exist despite filename suggestion
```

## Assurance Parity

| Source Manifest | Binary Manifest |
|-----------------|-----------------|
| Function name | Recovered/assigned name |
| Source file:line | Address + file offset |
| Signature | Deduced signature |
| Dependencies | Imports + syscalls |
| What doesn't exist | What doesn't exist |

Both prevent hallucinating nonexistent interfaces.

## Validation

Before writing interop code:

1. Check manifest for target function address
2. Verify calling convention matches your wrapper
3. Confirm parameter count/types
4. If not in manifest, DO NOT CALL — analyze first

---

*This methodology exists because binaries don't explain themselves. The manifest is ground truth.*
