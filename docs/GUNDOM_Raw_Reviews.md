# GUNDOM Ballistics Calculator - Raw Agent Reviews

**Date:** 2026-02-04  
**Projects Reviewed:** C:\GUNDOM, C:\BallisticsCalculator

---

# Table of Contents

1. [Ballistics Domain Review](#1-ballistics-domain-review)
2. [Assembly/Performance Review](#2-assemblyperformance-review)
3. [iOS/Swift Development Review](#3-iosswift-development-review)
4. [CI/CD Review](#4-cicd-review)
5. [Test Coverage Review](#5-test-coverage-review)

---

# 1. Ballistics Domain Review

**Agent:** ballistics 🎯  
**Focus:** Physics accuracy, drag models, atmospheric corrections

## Executive Summary

The GUNDOM project implements a high-quality external ballistics engine in C with iOS frontend support. The codebase demonstrates strong understanding of ballistic physics and follows industry references (JBM Ballistics, Applied Ballistics, Strelok Pro). However, I've identified several areas requiring attention ranging from minor improvements to physics accuracy concerns.

**Overall Assessment:** 7.5/10 - Solid foundation with some physics and implementation refinements needed.

## Critical Issues

### 🔴 CRITICAL: iOS app has corrupted drag tables

**File:** `BallisticsCalculator/C/ballistics.c`

The iOS app's drag tables contain **negative drag coefficient values** at high Mach numbers - this is physically impossible:

```c
// G1_DRAG table - Last entries show NEGATIVE drag coefficients!
0.5577, 0.5000, 0.4334, 0.3554,
0.2640, 0.1569, 0.0291, -0.1197, -0.2909, -0.4879, -0.7156, -0.9794,
-1.2858, ...
```

**Impact:** Any calculation at high Mach numbers (>4.0) will produce nonsensical results.

### 🟡 HIGH: G2/G5/G6/G8/GL models are approximations

**File:** `core/c/drag_models.c`, lines 130-161

Only G1 and G7 have real McCoy tables. Others use simple scaling factors:

```c
double drag_coefficient_g2(double mach) {
    double g1 = drag_coefficient_g1(mach);
    if (mach < 1.0) return g1 * 1.10;
    return g1 * 1.05;
}
```

**Problem:** The actual drag curves for these projectiles are NOT simple multiples of G1.

### 🟡 HIGH: Multi-BC curves not integrated

**File:** `core/c/ballistics.c`

The 5-point velocity-dependent BC feature exists (`bc_curve_interpolate()`) but isn't actually used in the main trajectory solver - it just uses a single BC value.

## Medium Priority Issues

1. **Coriolis horizontal formula differs from JBM** - GUNDOM matches Strelok Pro instead
2. **Mil definition ambiguity** - True milliradian (3.438"/100yd) vs NATO IPHY (3.6"/100yd)
3. **SIACCI retardation constant** - Empirically derived rather than physics-derived

## Positive Observations

- ✅ G1/G7 drag tables are accurate (McCoy/BRL data)
- ✅ Atmospheric model (ISA) is correctly implemented
- ✅ Kinetic energy formula is correct
- ✅ Wind drift uses proper lag-time method
- ✅ Good test coverage against JBM reference data
- ✅ Clean, well-documented C17 code

---

# 2. Assembly/Performance Review

**Agent:** asm ⚙️  
**Focus:** Low-level performance, SIMD opportunities, numeric precision

## Executive Summary

GUNDOM is a well-architected ballistics calculator with clean C code and existing ARM64 assembly optimizations. The codebase has significant opportunities for further low-level optimization, particularly in SIMD vectorization and memory layout.

**Estimated Impact with Full Optimization: 4-8x faster trajectory generation**

## Primary Hotspot

**File:** `core/c/drag_models.c`, lines 178-230

The `drag_velocity_at_distance()` function uses 1-foot step integration:

```c
while (remaining_distance > 0.0 && velocity > 0.0) {
    double step = (remaining_distance < step_size) ? remaining_distance : step_size;
    double retard = drag_retardation(model, velocity, bc, air_density, speed_of_sound);
    double dt = step / velocity;
    velocity -= retard * dt;
    remaining_distance -= step;
}
```

**Problems:**
- Sequential per-step computation (no SIMD)
- Function call overhead for `drag_retardation()` per iteration
- 3000+ iterations for 1000-yard trajectory at 1-ft steps

**Estimated Speedup with SIMD:** 3-4x

## Memory Layout Issues

**File:** `core/c/ballistics.h`

- `BallisticsInput` struct has padding gaps (4-6 bytes)
- Trajectory storage uses Array-of-Structures (AoS) - suboptimal for SIMD
- Recommend Structure-of-Arrays (SoA) for trajectory batches

## Existing ARM64 Assembly

**File:** `core/asm/ops_a64.s`

- ✅ Correct AAPCS64 calling convention
- ✅ Proper callee-saved register handling
- ⚠️ Calls libm `_sin`/`_cos` - 4 function calls per Coriolis computation
- ⚠️ No SIMD parallelism

**Opportunity:** Replace with NEON polynomial approximation for 2-4x Coriolis speedup

## Missing x86_64 Assembly

No AMD64/AVX2/AVX-512 optimizations exist - significant opportunity for Windows/Linux.

## Numeric Precision

Consistently uses `double` (64-bit) throughout - **correct choice** for ballistics accuracy (0.1 MOA at 1000yd).

## Priority Implementation Order

1. Compiler flag optimization (week 1)
2. AVX2/NEON intrinsics for drag batch (week 2)
3. Replace libm sincos with polynomial (week 3)
4. SoA trajectory batch allocation (week 4)
5. Full SIMD trajectory solver (week 5)

---

# 3. iOS/Swift Development Review

**Agent:** webdev 🌐  
**Focus:** iOS architecture, Swift code quality, UI/UX

## Executive Summary

GUNDOM is a **professional-grade ballistics calculator** iOS app with an exceptionally well-architected codebase. The C physics engine is production-ready (~85% feature parity with Strelok Pro), while the iOS UI layer is ~35% complete with many implemented features not yet exposed to users.

**Overall Assessment:** ⭐⭐⭐⭐ (4/5)

## Architecture

**Pattern:** MVVM + C Core

```
SwiftUI Views → ViewModel → C Physics Engine via Bridging Header
```

- ✅ Clean separation: UI (Swift) → Logic (C)
- ✅ Performance-critical code in optimized C17
- ✅ ARM64 SIMD via assembly for hot paths
- ✅ 8 specialized services (Profile, Location, Compass, Kestrel, etc.)

## Swift Code Quality

**BallisticsViewModel.swift** - ⭐⭐⭐⭐⭐
- Proper `@MainActor` isolation
- Combine publishers for reactive updates
- Debouncing to prevent excessive recalculation
- Safe C interop via `withUnsafeBytes`

## Data Persistence Gap

**Critical Finding:** SQLite schema exists and is comprehensive, but iOS app uses UserDefaults instead!

```sql
-- db/schema/ballistics_schema.sql (EXISTS but not wired)
CREATE TABLE rifles (...);
CREATE TABLE trajectory_base (...);  -- Pre-calculated trajectories
CREATE TABLE bullet_library (...);   -- 10 sample bullets seeded
```

**Recommendation:** Wire SQLite to iOS for trajectory caching and bullet libraries.

## UI Feature Parity

Per `GUNDOM_Complete_Feature_Audit.md`:
- **C Engine:** ~85% feature-complete vs Strelok Pro
- **iOS UI:** ~35% complete (many features implemented but not exposed)

**Hidden Features:**
- BC curve editor (implemented, under-utilized)
- Kestrel BLE integration (built, not prominent)
- GPS auto-fill (built, not prominent)

## Third-Party Dependencies

**Zero external dependencies** - excellent for security and maintenance.

## Accessibility Gaps

- ⚠️ No VoiceOver labels on custom components
- ⚠️ No Dynamic Type support (fixed font sizes)

---

# 4. CI/CD Review

**Agent:** cicd 🔄  
**Focus:** Build system, CI/CD, TestFlight automation

## Executive Summary

The GUNDOM project has **excellent, production-ready CI/CD infrastructure**. It has 8 comprehensive GitHub Actions workflows for building, testing, and deploying to TestFlight/App Store.

**Status: ✅ ALREADY EXCELLENT - No major changes needed**

## Existing Workflows

| Workflow | File | Purpose |
|----------|------|---------|
| Main CI | `ci.yml` | Matrix Debug/Release builds |
| Tests | `tests.yml` | Unit + physics tests |
| Benchmarks | `benchmarks.yml` | Performance validation |
| Release | `release.yml` | Tag-triggered builds |
| App Store | `app-store-release.yml` | TestFlight + App Store deployment |
| SQLite | `sqlite-verification.yml` | Custom SQLite build verification |

## Key Features

- Custom SQLite 3.51.2 build with optimized flags
- XCFramework creation for multi-platform support
- Matrix testing: macOS ARM64 + Ubuntu x64
- IPA creation with artifact upload
- 30-day artifact retention

## TestFlight Automation

**Fully automated** via `app-store-release.yml`:
- Manual trigger with version/build inputs
- Toggle for TestFlight upload
- App Store Connect API key authentication
- dSYM archiving for crash symbolication

## Suggested Enhancements (Low Priority)

1. Add CodeQL security scanning
2. Auto-TestFlight on `develop` branch
3. PR preview comments with artifact links

## BallisticsCalculator Note

`C:\BallisticsCalculator` has **no CI/CD** - appears to be older prototype. Consider archiving.

---

# 5. Test Coverage Review

**Agent:** testcov 🧪  
**Focus:** Test coverage gaps, testing strategy

## Executive Summary

GUNDOM has **strong existing test coverage** with a well-structured C test suite and XCTest integration. However, there are significant opportunities for improvement.

**Current Coverage Assessment: B+ (Good, with gaps)**

## Existing Coverage

**C Test Suite:** 14+ test files in `core/tests/`
- `test_ballistics.c` - 12 tests
- `test_physics_soundness.c` - 15+ tests (Coriolis t² scaling, ELR validation to 4000yd)
- `test_drag_models.c` - G1-G8 validation
- `test_units.c` - Complete unit conversion coverage

**XCTest:** `BallisticsEngineTests.swift`
- BC curve interpolation
- Truing workflow
- Atmosphere calculations

**CI Integration:**
- Dual-platform testing (macOS ARM64 + Ubuntu x64)
- Weekly benchmarks against JBM gold standard

## Reference Data

`jbm_reference_data.h` contains trajectories for:
- .308 Win 175gr SMK (G1 BC 0.495)
- 6.5 Creed 140gr ELD Match (G7 BC 0.273)
- .338 Lapua 300gr SMK (G1 BC 0.675)

## Gaps Identified

| Gap | Priority | Recommendation |
|-----|----------|----------------|
| Property-based testing | HIGH | Use Theft (C) / SwiftCheck (Swift) |
| Snapshot testing | HIGH | Golden files for trajectory outputs |
| Code coverage reporting | HIGH | Add gcov/llvm-cov to CI |
| UI Testing | MEDIUM | XCUITest for navigation flows |
| Fuzz testing | MEDIUM | libFuzzer for input boundaries |

## Top Property-Based Test Opportunities

1. **Velocity Decay:** `v(r₁) ≥ v(r₂)` for all r₁ < r₂
2. **Energy Invariant:** E > 0 for v > 0, E = 0 iff v = 0
3. **Unit Round-Trip:** `f⁻¹(f(x)) ≈ x` for all conversions
4. **Hemisphere Symmetry:** Coriolis(lat) = -Coriolis(-lat) horizontal

---

*End of Raw Reviews Document*
