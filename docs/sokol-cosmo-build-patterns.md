# Sokol & Cosmopolitan Build Patterns Analysis

> **Date:** 2026-02-06  
> **Purpose:** Document WORKING cross-platform build patterns from real-world projects  
> **Sources:** [github.com/floooh/sokol](https://github.com/floooh/sokol), [github.com/jart/cosmopolitan](https://github.com/jart/cosmopolitan)

---

## 1. Sokol CI Build System

### 1.1 GitHub Actions Workflow Structure

Sokol uses **parallel jobs per platform** with simple shell scripts:

```yaml
# .github/workflows/main.yml
name: "Build & Test"
on: [push, pull_request]

jobs:
    windows:
        runs-on: windows-latest
        steps:
        - uses: actions/checkout@main
        - name: prepare vulkan sdk
          uses: humbletim/setup-vulkan-sdk@main
          with:
            vulkan-query-version: 1.4.335.0
            vulkan-components: Vulkan-Headers, Vulkan-Loader
            vulkan-use-cache: true
        - name: test_win
          run: |
            cd tests
            test_win.cmd
          shell: cmd

    mac:
        runs-on: macos-latest
        steps:
        - uses: actions/checkout@main
        - uses: seanmiddleditch/gha-setup-ninja@master
        - name: test_macos
          run: cd tests && ./test_macos.sh

    ios:
        runs-on: macos-latest
        steps:
        - uses: actions/checkout@main
        - name: test_ios
          run: cd tests && ./test_ios.sh

    linux:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@main
        - uses: seanmiddleditch/gha-setup-ninja@master
        - name: prepare
          run: |
            sudo apt-get update
            sudo apt-get install libgl1-mesa-dev libegl1-mesa-dev \
              mesa-common-dev xorg-dev libasound-dev libvulkan-dev
        - name: test_linux
          run: cd tests && ./test_linux.sh

    emscripten:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@main
        - uses: seanmiddleditch/gha-setup-ninja@master
        - name: test_emscripten
          run: cd tests && ./test_emscripten.sh

    android:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@main
        - uses: seanmiddleditch/gha-setup-ninja@master
        - uses: actions/setup-java@v4
          with:
            distribution: 'zulu'
            java-version: '8'
        - name: test_android
          run: cd tests && ./test_android.sh
```

**Key Pattern: 6 Parallel Platform Jobs** — each runs independently, fail-fast per platform.

---

### 1.2 CMake Presets for Backend Selection

Sokol uses **CMake Presets** (`CMakePresets.json`) to define platform × backend combinations:

```json
{
    "version": 3,
    "configurePresets": [
        {
            "name": "linux_gl_debug",
            "generator": "Ninja",
            "binaryDir": "build/linux_gl_debug",
            "cacheVariables": {
                "SOKOL_BACKEND": "SOKOL_GLCORE",
                "CMAKE_BUILD_TYPE": "Debug"
            }
        },
        {
            "name": "linux_vulkan_release",
            "generator": "Ninja",
            "binaryDir": "build/linux_vulkan_release",
            "cacheVariables": {
                "SOKOL_BACKEND": "SOKOL_VULKAN",
                "CMAKE_BUILD_TYPE": "Release"
            }
        },
        {
            "name": "win_d3d11",
            "binaryDir": "build/win_d3d11",
            "cacheVariables": {
                "SOKOL_BACKEND": "SOKOL_D3D11"
            }
        },
        {
            "name": "emsc_webgl2_debug",
            "generator": "Ninja",
            "binaryDir": "build/emsc_webgl2_debug",
            "toolchainFile": "build/emsdk/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake",
            "cacheVariables": {
                "SOKOL_BACKEND": "SOKOL_GLES3",
                "CMAKE_BUILD_TYPE": "Debug"
            }
        },
        {
            "name": "android_debug",
            "generator": "Ninja",
            "binaryDir": "build/android_debug",
            "toolchainFile": "build/android_sdk/ndk-bundle/build/cmake/android.toolchain.cmake",
            "cacheVariables": {
                "SOKOL_BACKEND": "SOKOL_GLES3",
                "ANDROID_ABI": "armeabi-v7a",
                "ANDROID_PLATFORM": "android-30"
            }
        }
    ]
}
```

**Build commands are trivial:**
```bash
# Windows
cmake --preset win_d3d11
cmake --build --preset win_d3d11_debug

# Linux
cmake --preset linux_vulkan_debug
cmake --build --preset linux_vulkan_debug
```

---

### 1.3 CMakeLists.txt Platform Detection

```cmake
cmake_minimum_required(VERSION 3.20)
project(sokol-test)

# Backend selection via cache variable
set(SOKOL_BACKEND "SOKOL_DUMMY_BACKEND" CACHE STRING "Select 3D backend API")
set_property(CACHE SOKOL_BACKEND PROPERTY STRINGS 
    SOKOL_GLCORE SOKOL_METAL SOKOL_D3D11 SOKOL_VULKAN SOKOL_DUMMY_BACKEND)

# Platform detection
if (CMAKE_SYSTEM_NAME STREQUAL Emscripten)
    set(EMSCRIPTEN 1)
elseif (CMAKE_SYSTEM_NAME STREQUAL iOS)
    set(OSX_IOS 1)
elseif (CMAKE_SYSTEM_NAME STREQUAL Android)
    set(ANDROID 1)
elseif (CMAKE_SYSTEM_NAME STREQUAL Linux)
    set(LINUX 1)
elseif (CMAKE_SYSTEM_NAME STREQUAL Darwin)
    set(OSX_MACOS 1)
elseif (CMAKE_SYSTEM_NAME STREQUAL Windows)
    set(WINDOWS 1)
endif()

# Platform-specific libraries
if (EMSCRIPTEN)
    set(link_flags -sNO_FILESYSTEM=1 -sMALLOC=emmalloc --closure=1)
    if (SOKOL_BACKEND STREQUAL SOKOL_WGPU)
        set(link_flags ${link_flags} --use-port=emdawnwebgpu)
    else()
        set(link_flags ${link_flags} -sMIN_WEBGL_VERSION=2 -sMAX_WEBGL_VERSION=2)
    endif()
elseif (LINUX)
    find_package(Threads REQUIRED)
    if (SOKOL_BACKEND STREQUAL SOKOL_VULKAN)
        set(system_libs X11 Xi Xcursor vulkan asound dl m Threads::Threads)
    else()
        set(system_libs X11 Xi Xcursor GL asound dl m Threads::Threads)
    endif()
elseif (OSX_MACOS)
    set(system_libs "-framework QuartzCore" "-framework Cocoa" "-framework AudioToolbox")
    if (SOKOL_BACKEND STREQUAL SOKOL_METAL)
        set(system_libs ${system_libs} "-framework MetalKit" "-framework Metal")
    else()
        set(system_libs ${system_libs} "-framework OpenGL")
    endif()
elseif (WINDOWS)
    if (SOKOL_BACKEND STREQUAL SOKOL_VULKAN)
        set(system_libs vulkan-1)
    endif()
endif()
```

---

## 2. Cosmopolitan Build System

### 2.1 Core Philosophy: Build Once, Run Everywhere

Cosmopolitan uses **GNU Make** with a **monorepo structure**. Key insight: you build on Linux (or WSL), output runs on Windows/Mac/Linux/BSD without recompilation.

### 2.2 Mode-Based Build Configuration

```makefile
# build/config.mk - Build modes control optimization/debugging

# Default Mode: Optimized with debug info
ifeq ($(MODE),)
CONFIG_CCFLAGS += -O2 $(BACKTRACES)
CONFIG_CPPFLAGS += -DSYSDEBUG
endif

# Debug Mode: No optimization, ubsan, stack canaries
ifeq ($(MODE), dbg)
OVERRIDE_CFLAGS += -O0
CONFIG_CPPFLAGS += -DMODE_DBG -D__SANITIZE_UNDEFINED__
CONFIG_COPTS += -fsanitize=undefined
endif

# Release Mode: Optimized, stripped, no debug symbols
ifeq ($(MODE), rel)
CONFIG_CPPFLAGS += -DNDEBUG -DDWARFLESS
CONFIG_CCFLAGS += $(BACKTRACES) -O2
CONFIG_LDFLAGS += -S
endif

# Tiny Mode: Minimal size, YOLO
ifeq ($(MODE), tiny)
CONFIG_CPPFLAGS += -DTINY -DNDEBUG -DDWARFLESS
CONFIG_CCFLAGS += -Os -fno-align-functions -momit-leaf-frame-pointer
endif

# Architecture handling (x86_64 vs aarch64)
ifeq ($(MODE),)
ifeq ($(UNAME_M),aarch64)
MODE := aarch64
endif
endif
```

**Usage:**
```bash
make -j8 -O                    # Default optimized
make -j8 -O MODE=dbg           # Debug with sanitizers  
make -j8 -O MODE=rel           # Release
make -j8 -O MODE=tiny          # Minimal size
make -j8 -O MODE=aarch64       # Cross-compile to ARM64
```

---

### 2.3 Toolchain Auto-Download

```makefile
# Makefile - Toolchain setup
COSMOCC = .cosmocc/3.9.2
BOOTSTRAP = $(COSMOCC)/bin
TOOLCHAIN = $(COSMOCC)/bin/$(ARCH)-linux-cosmo-

# Auto-download if missing (build/download-cosmocc.sh handles this)
DOWNLOAD := $(shell build/download-cosmocc.sh $(COSMOCC) 3.9.2 <sha256>)

# Toolchain binaries
AS = $(TOOLCHAIN)as
CC = $(TOOLCHAIN)gcc
CXX = $(TOOLCHAIN)g++
LD = $(TOOLCHAIN)ld.bfd
AR = $(BOOTSTRAP)/ar.ape
```

---

### 2.4 Package-Based Dependencies (BUILD.mk Pattern)

Each directory has a `BUILD.mk` defining its package:

```makefile
# examples/BUILD.mk
PKGS += EXAMPLES

EXAMPLES_SRCS = $(wildcard examples/*.c) $(wildcard examples/*.cc)
EXAMPLES_OBJS = $(EXAMPLES_SRCS:%.c=o/$(MODE)/%.o)

# Declare dependencies on other packages
EXAMPLES_DIRECTDEPS = \
    LIBC_CALLS \
    LIBC_FMT \
    LIBC_STDIO \
    THIRD_PARTY_ZLIB \
    NET_HTTP

# Resolve transitive dependencies
EXAMPLES_DEPS := $(call uniq,$(foreach x,$(EXAMPLES_DIRECTDEPS),$($(x))))

# Package file for dependency tracking
o/$(MODE)/examples/examples.pkg: \
    $(EXAMPLES_OBJS) \
    $(foreach x,$(EXAMPLES_DIRECTDEPS),$($(x)_A).pkg)

# Link rule using APE (Actually Portable Executable)
o/$(MODE)/examples/%.dbg: \
    $(EXAMPLES_DEPS) \
    o/$(MODE)/examples/%.o \
    o/$(MODE)/examples/examples.pkg \
    $(CRT) $(APE_NO_MODIFY_SELF)
	@$(APELINK)
```

---

### 2.5 Pattern Rules (build/rules.mk)

```makefile
# Compile C to object
o/$(MODE)/%.o: %.c
	@$(COMPILE) -AOBJECTIFY.c $(OBJECTIFY.c) $(OUTPUT_OPTION) $<
	@$(COMPILE) -AFIXUPOBJ -wT$@ $(FIXUPOBJ) $@

# Compile C++ to object
o/$(MODE)/%.o: %.cc
	@$(COMPILE) -AOBJECTIFY.cxx $(OBJECTIFY.cxx) $(OUTPUT_OPTION) $<
	@$(COMPILE) -AFIXUPOBJ -wT$@ $(FIXUPOBJ) $@

# Create .dbg → strip to final binary
o/$(MODE)/%: o/$(MODE)/%.dbg
	@$(MAKE_OBJCOPY)

# Archive creation
o/%.a:
	$(file >$(TMPDIR)/$(subst /,_,$@),$^)
	@$(COMPILE) -AARCHIVE -wT$@ $(AR) $(ARFLAGS) $@ @$(TMPDIR)/$(subst /,_,$@)

# Run tests
o/$(MODE)/%.runs: o/$(MODE)/%
	@$(COMPILE) -ACHECK -wtT$@ $< $(TESTARGS)
```

---

## 3. Cross-Platform Build Patterns to Follow

### 3.1 ✅ Sokol Patterns (Recommended for Graphics/UI)

| Pattern | Use When |
|---------|----------|
| **CMake Presets** | Managing platform × backend matrix |
| **Parallel CI jobs** | Testing all platforms simultaneously |
| **Toolchain files** | Cross-compiling (Emscripten, Android NDK) |
| **Backend defines** | Switching graphics APIs at compile time |
| **Simple shell scripts** | Platform-specific build sequences |

### 3.2 ✅ Cosmopolitan Patterns (Recommended for CLI/Server)

| Pattern | Use When |
|---------|----------|
| **MODE variable** | Switching debug/release/tiny builds |
| **Package dependencies** | Managing large codebases |
| **Pattern rules** | Consistent compilation across file types |
| **Auto-downloading toolchain** | Reproducible builds |
| **APE linking** | Single binary for all platforms |

### 3.3 Combined Approach for OpenClaw

```yaml
# .github/workflows/build.yml (Sokol-style parallel jobs)
jobs:
  linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Cosmocc
        run: ./scripts/setup-cosmocc.sh
      - name: Build
        run: make -j$(nproc) MODE=${{ matrix.mode }}
    strategy:
      matrix:
        mode: [default, dbg, rel, tiny]

  # Cross-compile in parallel
  aarch64:
    runs-on: ubuntu-latest  
    steps:
      - uses: actions/checkout@v4
      - run: make -j$(nproc) MODE=aarch64
```

---

## 4. Practical Implementation Notes

### 4.1 What Actually Works

1. **Linux-only build host** — Cosmopolitan requires Linux/WSL for building
2. **Parallel CI jobs** — Sokol's approach: one job per major platform
3. **CMake presets** — Far cleaner than complex CMakeLists conditionals
4. **Mode variables** — Simple flag switches entire build configuration
5. **Auto-download toolchain** — Eliminates "works on my machine"

### 4.2 Avoid These

1. ❌ Matrix builds across too many dimensions (explosion of combinations)
2. ❌ Platform detection via complex CMake scripts
3. ❌ Hardcoded paths to SDKs
4. ❌ Manual dependency management

### 4.3 SDK/Dependency Setup

**Sokol approach (external actions):**
```yaml
- uses: humbletim/setup-vulkan-sdk@main
- uses: seanmiddleditch/gha-setup-ninja@master
```

**Cosmopolitan approach (apt-get + auto-download):**
```bash
sudo apt-get install libgl1-mesa-dev libegl1-mesa-dev
./build/download-cosmocc.sh  # Auto-download verified toolchain
```

---

## 5. File Structure Reference

```
# Sokol structure (CMake-centric)
├── .github/workflows/main.yml
├── tests/
│   ├── CMakeLists.txt
│   ├── CMakePresets.json
│   ├── test_win.cmd
│   ├── test_linux.sh
│   ├── test_macos.sh
│   └── test_emscripten.sh

# Cosmopolitan structure (Make-centric)
├── Makefile
├── build/
│   ├── config.mk          # Mode definitions
│   ├── rules.mk           # Pattern rules
│   ├── functions.mk       # Helper functions
│   └── download-cosmocc.sh
├── examples/BUILD.mk      # Package definition
├── libc/BUILD.mk
└── .cosmocc/              # Auto-downloaded toolchain
```

---

## 6. Quick Reference Commands

```bash
# Sokol-style
cmake --preset linux_vulkan_debug && cmake --build --preset linux_vulkan_debug

# Cosmopolitan-style  
make -j8 -O MODE=dbg o//examples/hello
make -j8 -O MODE=rel
make -j8 -O MODE=aarch64

# Test a specific target
make o//test/libc/calls/openbsd_test.runs
```

---

**Document Version:** 1.0  
**Analyzed Repositories:**  
- Sokol: commit @master (2026-02-06)  
- Cosmopolitan: commit @master (2026-02-06)
