# TOOLS.md - Cosmo Agent Local Notes

## Local Toolchain Paths

### cosmocc Toolchain
- **Location:** `C:\mhi-procurement\vendor\cosmocc\`
- **Binaries:** `vendor/cosmocc/bin/` (need .com extension on Windows or use via bash)
- **Include:** `vendor/cosmocc/include/`
- **Lib:** `vendor/cosmocc/lib/`

### Git Bash (for running shell scripts on Windows)
- **Path:** `C:\Program Files\Git\bin\bash.exe`
- **Usage:** `& "C:\Program Files\Git\bin\bash.exe" -c "command here"`

### Local Projects

| Project | Path | Description |
|---------|------|-------------|
| mhi-procurement | `C:\mhi-procurement` | GUI procurement app (CImGui + Sokol + SQLite) |
| tedit-cosmo | `C:\tedit-cosmo` | Teditor clone (text editor) |
| e9studio | `C:\e9studio` | Binary analysis tool |
| cosmo-disasm | `C:\cosmo-disasm` | Disassembler |
| apeswarm | `C:\apeswarm` | Binaryen.wasm composition platform |

### Sokol Integration Notes

**Current API (Aug 2025+):**
- Use `sg_view` / `sg_make_view()` (NOT `sg_attachments`)
- Shim location: `C:\mhi-procurement\shims\sokol\`
- Platform headers: `sokol_linux.h`, `sokol_windows.h`
- X11 stubs: `shims/linux/X11/`

**Build Test (verified working):**
```powershell
cd C:\mhi-procurement
& "C:\Program Files\Git\bin\bash.exe" -c "vendor/cosmocc/bin/cosmocc -c -O2 -Ivendor/sokol -Ishims/sokol -DSOKOL_GLCORE shims/sokol/sokol_cosmo.c -o build/test.o"
```

### llamafile (Local LLM)

For simple code generation tasks, use the local Qwen model:
- **Binary:** `C:\Users\user\.openclaw\workspace\bin\llamafile.exe`
- **Model:** `C:\Users\user\.openclaw\workspace\models\qwen2.5-7b-instruct-q3_k_m.gguf`
- Delegate boilerplate/formatting to Qwen, save Claude tokens for complex reasoning.

---

Update this file with project-specific discoveries and paths.
