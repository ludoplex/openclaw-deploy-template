# Cosmokramerpolitan Source Manifest

Generated: 2026-02-11
Source: https://github.com/ludoplex/cosmokramerpolitan (fork of jart/cosmopolitan)
Path: `C:\cosmokramerpolitan`

## Overview

Cosmopolitan Libc makes C/C++ a build-once run-anywhere language. Outputs POSIX-approved polyglot format (APE) that runs natively on Linux + Mac + Windows + FreeBSD + OpenBSD + NetBSD + BIOS.

**This is the base layer** for all cosmo-* projects.

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `ape/` | Actually Portable Executable loader |
| `libc/` | Cosmopolitan C library |
| `build/` | Build system and scripts |
| `ctl/` | Control utilities |
| `dsp/` | Digital signal processing |
| `net/` | Networking |
| `third_party/` | Bundled third-party libs |
| `tool/` | Development tools |
| `examples/` | Example programs |
| `test/` | Test suite |

## Key Components

### APE Loader (`ape/`)
| File | Purpose |
|------|---------|
| `ape.S` | APE executable format implementation |
| `ape-loader.c` | Runtime loader |
| `apeinstall.sh` | APE installation script |

### Libc (`libc/`)
| Directory | Purpose |
|-----------|---------|
| `calls/` | System call wrappers |
| `fmt/` | Formatting (printf, etc.) |
| `intrin/` | Compiler intrinsics |
| `mem/` | Memory management |
| `nexgen32e/` | x86-64 specific |
| `nt/` | Windows NT compatibility |
| `runtime/` | Runtime initialization |
| `sock/` | Socket implementation |
| `stdio/` | Standard I/O |
| `str/` | String functions |
| `sysv/` | SysV ABI |
| `thread/` | Threading |
| `x/` | Extended functionality |

### Tools (`tool/`)
| Tool | Purpose |
|------|---------|
| `cosmocc/` | Cosmopolitan C Compiler wrapper |
| `build/` | Build utilities |
| `curl/` | HTTP client |
| `net/` | Network utilities |

### Third Party (`third_party/`)
| Library | Purpose |
|---------|---------|
| `dlmalloc/` | Memory allocator |
| `mbedtls/` | TLS/crypto |
| `musl/` | musl libc portions |
| `python/` | Python interpreter |
| `sqlite3/` | SQLite database |
| `zlib/` | Compression |
| `lua/` | Lua interpreter |
| `quickjs/` | JavaScript engine |

## Build System

```bash
# Download cosmocc automatically
make

# Build specific target
make o//examples/hello.com

# Run tests
make check

# Install to prefix
make install PREFIX=/opt/cosmos
```

## Compiler Usage

```bash
# Add to PATH
export PATH="/path/to/cosmopolitan/bin:$PATH"

# Compile
cosmocc -o hello hello.c

# Cross-compile for specific arch
x86_64-unknown-cosmo-cc -o hello hello.c
aarch64-unknown-cosmo-cc -o hello hello.c
```

## Runtime Features

```bash
# System call tracing
./program --strace

# Function call tracing
./program --ftrace

# Disable ASLR
./program --disable-aslr
```

## Platform Detection (Runtime)

```c
#include <cosmopolitan.h>

if (IsLinux()) { /* Linux-specific */ }
if (IsWindows()) { /* Windows-specific */ }
if (IsXnu()) { /* macOS-specific */ }
if (IsBsd()) { /* BSD-specific */ }
if (IsOpenbsd()) { /* OpenBSD-specific */ }
```

## Key Patterns

### ZipOS (Embedded Assets)
```bash
# Embed files in executable
zip -r program.com /zip/assets/
# Access at runtime via /zip/assets/...
```

### Static Linking
```makefile
LDFLAGS = -static
```

### dlopen for System Libs Only
```c
// Only for X11, OpenGL, etc.
void *lib = cosmo_dlopen("libX11.so.6", RTLD_LAZY);
```

## Integration Points

| Project | Uses |
|---------|------|
| cosmo-sokol | GUI apps with cosmo-sokol pattern |
| tedit-cosmo | Editor built on cosmokramerpolitan |
| e9studio | Binary rewriter |
| cosmo-disasm | Disassembler library |
| llamafile | LLM inference engine |
| cosmo-bsd | BSD-based OS |

## What Does NOT Exist

- ❌ No C++ exceptions (optional, disabled by default)
- ❌ No RTTI
- ❌ No dynamic linking (except dlopen for system libs)
- ❌ No 32-bit Windows
- ❌ No ARM32

## Documentation

- Website: https://justine.lol/cosmopolitan/
- API Docs: https://justine.lol/cosmopolitan/documentation.html
- APE Format: https://justine.lol/ape.html
- Downloads: https://cosmo.zip/pub/cosmocc/

---

*This manifest is ground truth. The foundation of the portable RE stack.*
