# Cross-Platform Testing Patterns: Sokol & Cosmopolitan

*Research conducted: 2026-02-06*

## Executive Summary

Both Sokol and Cosmopolitan approach cross-platform testing differently based on their distinct architectures:

- **Sokol**: Tests the *same code* compiled separately for each platform via CI matrix
- **Cosmopolitan**: Tests *single fat binaries* that run on all platforms natively

## 1. Sokol's Cross-Platform Testing Approach

### Architecture Overview

Sokol is a collection of single-header C libraries for graphics, audio, input, etc. Cross-platform compatibility is achieved through **compile-time backend selection** and **platform-specific code paths**.

### Testing Strategy

#### 1.1 CI Matrix Testing

Sokol uses GitHub Actions to test across 6 target platforms:

```yaml
# .github/workflows/main.yml
jobs:
    windows:
        runs-on: windows-latest
    mac:
        runs-on: macos-latest
    ios:
        runs-on: macos-latest
    linux:
        runs-on: ubuntu-latest
    emscripten:
        runs-on: ubuntu-latest
    android:
        runs-on: ubuntu-latest
```

Each platform runs its own test script (e.g., `test_linux.sh`, `test_win.cmd`).

#### 1.2 Build Configuration Variants

Linux alone tests **8 different configurations**:

```bash
# tests/test_linux.sh
build linux_gl_debug linux_gl_debug
build linux_gl_release linux_gl_release
build linux_vulkan_debug linux_vulkan_debug
build linux_vulkan_release linux_vulkan_release
build linux_gles3_debug linux_gles3_debug
build linux_gles3_release linux_gles3_release
build linux_gl_egl_debug linux_gl_egl_debug
build linux_gl_egl_release linux_gl_egl_release
```

#### 1.3 Two-Layer Test Architecture

**Compile Tests** (tests/compile/):
- Verify that headers compile cleanly with both C and C++
- Test both with and without sokol_app integration
- Ensure no warnings with `-Wall -Wextra -Werror`

```cmake
# Compile both C and C++ versions
add_executable(sokol-compiletest-c ${c_sources})
add_executable(sokol-compiletest-cxx ${cxx_sources})
```

**Functional Tests** (tests/functional/):
- Use a `SOKOL_DUMMY_BACKEND` for headless testing
- Unit tests for each module (sokol_gfx_test.c, sokol_audio_test.c, etc.)
- Use [utest.h](https://github.com/sheredom/utest.h) framework

```c
// tests/functional/sokol_gfx_test.c
#include "force_dummy_backend.h"
#define SOKOL_IMPL
#include "sokol_gfx.h"
#include "utest.h"

UTEST(sokol_gfx, init_shutdown) {
    setup(&(sg_desc){0});
    T(sg_isvalid());
    sg_shutdown();
    T(!sg_isvalid());
}

UTEST(sokol_gfx, query_backend) {
    setup(&(sg_desc){0});
    T(sg_query_backend() == SG_BACKEND_DUMMY);
    sg_shutdown();
}
```

#### 1.4 Key Testing Patterns

1. **Dummy Backend**: Mock graphics backend for CI testing without GPU
2. **Resource Lifecycle Tests**: Alloc → Init → Use → Destroy cycles
3. **Pool Exhaustion Tests**: Verify behavior when resources depleted
4. **State Query Tests**: Verify resource states through transitions

---

## 2. Cosmopolitan's Fat Binary Testing Approach

### Architecture Overview

Cosmopolitan creates "Actually Portable Executables" (APE) - single binaries that run on Linux, macOS, Windows, FreeBSD, OpenBSD, and NetBSD without modification.

### Testing Strategy

#### 2.1 Build Mode Matrix

```yaml
# .github/workflows/build.yml
strategy:
  matrix:
    mode: ["", tiny, rel, tinylinux]
```

- Empty mode: Full-featured build
- `tiny`: Minimal size, cross-platform
- `rel`: Release optimized
- `tinylinux`: Linux-only minimal (tests isolation)

#### 2.2 Test Organization (Makefile-based)

Tests organized by libc subsystem:

```makefile
# test/libc/calls/BUILD.mk
TEST_LIBC_CALLS_SRCS := $(wildcard test/libc/calls/*.c)
TEST_LIBC_CALLS_SRCS_TEST := $(filter %_test.c,$(TEST_LIBC_CALLS_SRCS))
```

Test categories include:
- `test/libc/calls/` - System calls
- `test/libc/thread/` - Threading
- `test/libc/sock/` - Networking
- `test/libc/mem/` - Memory management
- `test/posix/` - POSIX compliance
- `test/ctl/` - C++ STL (cosmopolitan template library)

#### 2.3 Custom Test Framework

Cosmopolitan has its own `testlib.h` with Google Test-style macros:

```c
// libc/testlib/testlib.h
#define TEST(SUITE, NAME) ...
#define ASSERT_EQ(WANT, GOT, ...) ...
#define ASSERT_SYS(ERRNO, WANT, GOT, ...) ...  // syscall + errno check
#define EXPECT_STREQ(WANT, GOT) ...
#define FIXTURE(SUITE, NAME) ...  // For parameterized tests
#define BENCH(SUITE, NAME) ...    // Benchmarks
```

Special features:
- `ASSERT_SYS`: Checks both return value AND errno
- `testlib_enable_tmp_setup_teardown()`: Auto-creates test directories
- `FIXTURE`: Runs all tests multiple times with different configurations

#### 2.4 Test Sandboxing

Tests run with security constraints:

```makefile
# Per-test security configuration
o/$(MODE)/test/libc/calls/pledge_test.runs: private .PLEDGE = unveil
o/$(MODE)/test/libc/calls/poll_test.runs: private .PLEDGE = inet
o/$(MODE)/test/libc/calls/specialfile_test.runs: \
    private .UNVEIL = r:/dev/random r:/dev/urandom
```

#### 2.5 Example: Minimal Cross-Platform Test

```c
// test/posix/signal_test.c
#include <signal.h>
#include <stdlib.h>

volatile sig_atomic_t signal_received = 0;

void signal_handler(int signum) {
  signal_received = 1;
}

int main() {
  struct sigaction sa;
  sa.sa_handler = signal_handler;
  sigemptyset(&sa.sa_mask);
  sa.sa_flags = 0;

  if (sigaction(SIGUSR1, &sa, NULL) == -1) exit(1);
  if (raise(SIGUSR1) != 0) exit(2);
  exit(signal_received == 1 ? 0 : 3);
}
```

This single binary test works on all 6 supported OSes.

---

## 3. Recommendations for MHI Procurement Engine

Based on the patterns from Sokol and Cosmopolitan, here are recommended testing strategies:

### 3.1 If Building Traditional Cross-Platform (Sokol-style)

```yaml
# CI Matrix
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
    build_type: [Debug, Release]
```

Key patterns:
- **Dummy/Mock Backends**: Test business logic without platform dependencies
- **Compile Tests**: Ensure code compiles on all targets with strict warnings
- **Feature Flag Matrix**: Test different configurations (e.g., SQLite vs PostgreSQL)

### 3.2 If Building Fat Binaries (Cosmopolitan-style)

Use cosmocc compiler and test on single CI runner:

```bash
cosmocc -o procurement_engine main.c
./procurement_engine --strace  # Debug syscalls
```

Key patterns:
- **Single Binary Tests**: Write tests as standalone executables
- **Exit Code Signaling**: Use distinct exit codes for different failures
- **Syscall Compatibility Tests**: Verify OS abstraction layer works

### 3.3 Unified Testing Patterns (Both Approaches)

| Pattern | Description | Example |
|---------|-------------|---------|
| **Lifecycle Tests** | Test resource create/use/destroy | Pool exhaustion handling |
| **State Machine Tests** | Verify state transitions | Order: Draft→Submitted→Approved |
| **Error Condition Tests** | Test failure paths | Invalid input, resource limits |
| **Integration Tests** | Cross-module interaction | API→Service→Database |
| **Security Sandboxing** | Run tests with minimal permissions | pledge/unveil on OpenBSD |

### 3.4 Recommended Test File Structure

```
tests/
├── unit/                    # Fast, isolated tests
│   ├── core/
│   │   ├── order_test.c
│   │   └── inventory_test.c
│   └── mocks/
│       └── database_mock.h
├── integration/             # Cross-module tests
│   └── procurement_flow_test.c
├── compile/                 # Compilation verification
│   ├── c89_compat_test.c
│   └── cpp_compat_test.cc
├── platform/                # OS-specific tests
│   ├── posix_test.c
│   └── win32_test.c
└── BUILD.mk or CMakeLists.txt
```

### 3.5 Recommended Test Framework

For C procurement engine, consider:

1. **utest.h** (single header, used by Sokol)
2. **Greatest** (single header, tap/junit output)
3. **Custom testlib** (Cosmopolitan's approach, full control)

Minimum viable test macro set:
```c
#define TEST(suite, name) void suite##_##name(void)
#define ASSERT_TRUE(x)    if(!(x)) { fail(__LINE__); }
#define ASSERT_EQ(a, b)   if((a) != (b)) { fail(__LINE__); }
#define ASSERT_STREQ(a,b) if(strcmp(a,b)) { fail(__LINE__); }
```

### 3.6 CI Configuration Template

```yaml
name: Test
on: [push, pull_request]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: cmake --preset release && cmake --build --preset release
      - name: Test
        run: ctest --preset release --output-on-failure
```

---

## 4. Key Takeaways

| Aspect | Sokol | Cosmopolitan | MHI Recommendation |
|--------|-------|--------------|-------------------|
| **Binary Strategy** | Platform-specific builds | Single fat binary | Depends on deployment |
| **CI Approach** | Matrix of runners | Single runner, multiple modes | Matrix for traditional |
| **Mock Strategy** | Dummy backend | Real syscalls, sandboxed | Hybrid approach |
| **Test Framework** | utest.h | Custom testlib | utest.h for simplicity |
| **Error Handling** | State queries | Exit codes + errno | State queries + logging |

---

## References

- [Sokol Repository](https://github.com/floooh/sokol)
- [Cosmopolitan Repository](https://github.com/jart/cosmopolitan)
- [Sokol Tests](https://github.com/floooh/sokol/tree/master/tests)
- [Cosmopolitan testlib.h](https://github.com/jart/cosmopolitan/blob/master/libc/testlib/testlib.h)
- [APE Documentation](https://justine.lol/ape.html)
