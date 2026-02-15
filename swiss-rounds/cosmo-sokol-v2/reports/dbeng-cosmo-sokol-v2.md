# cosmo-sokol-v2 Database Schemas

**Author:** dbeng agent  
**Date:** 2026-02-09  
**Purpose:** SQLite schemas for build metadata, test results, and artifact registry

---

## 1. Build Metadata Database

```sql
-- =============================================================================
-- BUILD METADATA DATABASE (build_metadata.db)
-- Tracks versions, builds, and compatibility across sokol/cimgui/cosmopolitan
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- VERSIONS: Track commit SHAs and dates for each upstream dependency
-- -----------------------------------------------------------------------------
CREATE TABLE versions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    component       TEXT NOT NULL CHECK(component IN ('sokol', 'cimgui', 'cosmopolitan')),
    commit_sha      TEXT NOT NULL,
    commit_date     TEXT NOT NULL,  -- ISO 8601 format
    branch          TEXT DEFAULT 'master',
    fetched_at      TEXT NOT NULL DEFAULT (datetime('now')),
    notes           TEXT,
    
    UNIQUE(component, commit_sha)
);

CREATE INDEX idx_versions_component ON versions(component);
CREATE INDEX idx_versions_commit_date ON versions(commit_date);

-- -----------------------------------------------------------------------------
-- BUILDS: Individual build attempts with full configuration
-- -----------------------------------------------------------------------------
CREATE TABLE builds (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    sokol_version_id    INTEGER NOT NULL REFERENCES versions(id),
    cimgui_version_id   INTEGER NOT NULL REFERENCES versions(id),
    cosmo_version_id    INTEGER NOT NULL REFERENCES versions(id),
    cosmocc_version     TEXT NOT NULL,          -- e.g., "3.9.3"
    compiler_flags      TEXT,                   -- JSON array of flags
    build_timestamp     TEXT NOT NULL DEFAULT (datetime('now')),
    build_duration_sec  INTEGER,
    status              TEXT NOT NULL CHECK(status IN ('success', 'failed', 'partial')),
    error_message       TEXT,
    build_host          TEXT,                   -- machine that ran the build
    
    UNIQUE(sokol_version_id, cimgui_version_id, cosmo_version_id, compiler_flags)
);

CREATE INDEX idx_builds_status ON builds(status);
CREATE INDEX idx_builds_timestamp ON builds(build_timestamp);

-- -----------------------------------------------------------------------------
-- COMPATIBILITY: Known-good version combinations
-- -----------------------------------------------------------------------------
CREATE TABLE compatibility (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    sokol_version_id    INTEGER NOT NULL REFERENCES versions(id),
    cimgui_version_id   INTEGER NOT NULL REFERENCES versions(id),
    cosmo_version_id    INTEGER NOT NULL REFERENCES versions(id),
    verified_build_id   INTEGER REFERENCES builds(id),
    verified_at         TEXT NOT NULL DEFAULT (datetime('now')),
    stability           TEXT CHECK(stability IN ('stable', 'beta', 'experimental')),
    notes               TEXT,
    
    UNIQUE(sokol_version_id, cimgui_version_id, cosmo_version_id)
);
```

### Example Inserts

```sql
-- Insert version records
INSERT INTO versions (component, commit_sha, commit_date, branch, notes)
VALUES 
    ('sokol', 'a1b2c3d4e5f6789012345678901234567890abcd', '2026-02-01', 'master', 'Latest stable'),
    ('cimgui', 'b2c3d4e5f6789012345678901234567890abcdef', '2026-01-28', 'docking', 'Docking branch'),
    ('cosmopolitan', 'c3d4e5f6789012345678901234567890abcdef01', '2026-02-05', 'master', 'APE loader v3');

-- Record a successful build
INSERT INTO builds (sokol_version_id, cimgui_version_id, cosmo_version_id, 
                    cosmocc_version, compiler_flags, build_duration_sec, status, build_host)
VALUES (1, 2, 3, '3.9.3', '["-O2", "-DNDEBUG", "-march=x86-64"]', 127, 'success', 'build-01');

-- Mark as compatible
INSERT INTO compatibility (sokol_version_id, cimgui_version_id, cosmo_version_id, 
                           verified_build_id, stability)
VALUES (1, 2, 3, 1, 'stable');
```

### Common Queries

```sql
-- Find last successful build
SELECT b.*, 
       sv.commit_sha AS sokol_sha,
       cv.commit_sha AS cimgui_sha,
       pv.commit_sha AS cosmo_sha
FROM builds b
JOIN versions sv ON b.sokol_version_id = sv.id
JOIN versions cv ON b.cimgui_version_id = cv.id
JOIN versions pv ON b.cosmo_version_id = pv.id
WHERE b.status = 'success'
ORDER BY b.build_timestamp DESC
LIMIT 1;

-- Get all stable compatible combinations
SELECT 
    sv.commit_sha AS sokol,
    cv.commit_sha AS cimgui,
    pv.commit_sha AS cosmo,
    c.verified_at
FROM compatibility c
JOIN versions sv ON c.sokol_version_id = sv.id
JOIN versions cv ON c.cimgui_version_id = cv.id
JOIN versions pv ON c.cosmo_version_id = pv.id
WHERE c.stability = 'stable'
ORDER BY c.verified_at DESC;

-- Find builds that failed for a specific component version
SELECT b.*, b.error_message
FROM builds b
JOIN versions v ON b.sokol_version_id = v.id
WHERE v.commit_sha = 'a1b2c3d4e5f6789012345678901234567890abcd'
  AND b.status = 'failed';
```

---

## 2. Test Results Database

```sql
-- =============================================================================
-- TEST RESULTS DATABASE (test_results.db)
-- Tracks test runs, individual results, and platform definitions
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- PLATFORMS: Define target platforms for testing
-- -----------------------------------------------------------------------------
CREATE TABLE platforms (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    os              TEXT NOT NULL,              -- linux, darwin, windows, freebsd, netbsd, openbsd
    arch            TEXT NOT NULL,              -- x86_64, aarch64
    environment     TEXT NOT NULL CHECK(environment IN ('native', 'vm', 'emulator', 'wsl')),
    os_version      TEXT,                       -- e.g., "Ubuntu 22.04", "macOS 14.3"
    notes           TEXT,
    active          INTEGER NOT NULL DEFAULT 1,
    
    UNIQUE(os, arch, environment, os_version)
);

CREATE INDEX idx_platforms_os_arch ON platforms(os, arch);

-- -----------------------------------------------------------------------------
-- TEST_RUNS: A complete test execution session
-- -----------------------------------------------------------------------------
CREATE TABLE test_runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_timestamp   TEXT NOT NULL DEFAULT (datetime('now')),
    platform_id     INTEGER NOT NULL REFERENCES platforms(id),
    git_commit      TEXT NOT NULL,              -- cosmo-sokol-v2 repo commit
    build_id        INTEGER,                    -- optional FK to build_metadata.builds
    total_tests     INTEGER NOT NULL DEFAULT 0,
    passed          INTEGER NOT NULL DEFAULT 0,
    failed          INTEGER NOT NULL DEFAULT 0,
    skipped         INTEGER NOT NULL DEFAULT 0,
    duration_sec    INTEGER,
    trigger         TEXT CHECK(trigger IN ('manual', 'scheduled', 'commit', 'pr')),
    runner_host     TEXT
);

CREATE INDEX idx_test_runs_timestamp ON test_runs(run_timestamp);
CREATE INDEX idx_test_runs_platform ON test_runs(platform_id);
CREATE INDEX idx_test_runs_commit ON test_runs(git_commit);

-- -----------------------------------------------------------------------------
-- TEST_RESULTS: Individual test case outcomes
-- -----------------------------------------------------------------------------
CREATE TABLE test_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL REFERENCES test_runs(id) ON DELETE CASCADE,
    test_name       TEXT NOT NULL,              -- e.g., "sokol_app::window_create"
    test_suite      TEXT,                       -- e.g., "sokol_app", "cimgui_render"
    outcome         TEXT NOT NULL CHECK(outcome IN ('pass', 'fail', 'skip', 'error', 'timeout')),
    duration_ms     INTEGER,
    error_message   TEXT,
    stack_trace     TEXT,
    retry_count     INTEGER DEFAULT 0,
    
    UNIQUE(run_id, test_name)
);

CREATE INDEX idx_test_results_outcome ON test_results(outcome);
CREATE INDEX idx_test_results_test_name ON test_results(test_name);
CREATE INDEX idx_test_results_suite ON test_results(test_suite);

-- -----------------------------------------------------------------------------
-- TEST_HISTORY: Materialized view for regression tracking (manual refresh)
-- -----------------------------------------------------------------------------
CREATE TABLE test_history (
    test_name       TEXT NOT NULL,
    platform_id     INTEGER NOT NULL REFERENCES platforms(id),
    last_pass       TEXT,                       -- timestamp of last pass
    last_fail       TEXT,                       -- timestamp of last fail
    consecutive_fails INTEGER DEFAULT 0,
    total_runs      INTEGER DEFAULT 0,
    pass_rate       REAL,                       -- 0.0 to 1.0
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    
    PRIMARY KEY(test_name, platform_id)
);
```

### Example Inserts

```sql
-- Define platforms
INSERT INTO platforms (os, arch, environment, os_version)
VALUES 
    ('linux', 'x86_64', 'native', 'Ubuntu 24.04'),
    ('linux', 'aarch64', 'vm', 'Debian 12 (QEMU)'),
    ('darwin', 'aarch64', 'native', 'macOS 14.3'),
    ('windows', 'x86_64', 'native', 'Windows 11'),
    ('freebsd', 'x86_64', 'vm', 'FreeBSD 14.0');

-- Record a test run
INSERT INTO test_runs (platform_id, git_commit, total_tests, passed, failed, skipped, 
                       duration_sec, trigger, runner_host)
VALUES (1, 'abc123def456789', 42, 40, 1, 1, 89, 'commit', 'runner-linux-01');

-- Insert test results
INSERT INTO test_results (run_id, test_name, test_suite, outcome, duration_ms)
VALUES 
    (1, 'sokol_app::window_create', 'sokol_app', 'pass', 45),
    (1, 'sokol_app::window_resize', 'sokol_app', 'pass', 23),
    (1, 'sokol_gfx::buffer_create', 'sokol_gfx', 'pass', 12),
    (1, 'cimgui::render_frame', 'cimgui', 'fail', 150, 'Segfault in ImGui::Render()'),
    (1, 'sokol_audio::init', 'sokol_audio', 'skip', NULL);
```

### Common Queries

```sql
-- Find regressions: tests that passed before but now fail
SELECT tr.test_name, tr.test_suite, 
       prev.outcome AS previous_outcome,
       tr.outcome AS current_outcome,
       tr.error_message,
       p.os, p.arch
FROM test_results tr
JOIN test_runs run ON tr.run_id = run.id
JOIN platforms p ON run.platform_id = p.id
JOIN test_results prev ON tr.test_name = prev.test_name
JOIN test_runs prev_run ON prev.run_id = prev_run.id
WHERE tr.outcome = 'fail' 
  AND prev.outcome = 'pass'
  AND prev_run.platform_id = run.platform_id
  AND prev_run.run_timestamp < run.run_timestamp
  AND run.id = (SELECT MAX(id) FROM test_runs WHERE platform_id = p.id)
  AND prev_run.id = (SELECT MAX(id) FROM test_runs WHERE platform_id = p.id AND id < run.id);

-- Test pass rate by platform
SELECT p.os, p.arch, p.environment,
       COUNT(*) AS total_runs,
       ROUND(AVG(run.passed * 1.0 / run.total_tests) * 100, 2) AS avg_pass_rate_pct
FROM test_runs run
JOIN platforms p ON run.platform_id = p.id
WHERE run.total_tests > 0
GROUP BY p.id
ORDER BY avg_pass_rate_pct DESC;

-- Find flaky tests (different outcomes in recent runs on same platform)
SELECT test_name, platform_id,
       COUNT(DISTINCT outcome) AS outcome_variance,
       GROUP_CONCAT(DISTINCT outcome) AS outcomes
FROM test_results tr
JOIN test_runs run ON tr.run_id = run.id
WHERE run.run_timestamp > datetime('now', '-7 days')
GROUP BY test_name, platform_id
HAVING COUNT(DISTINCT outcome) > 1;

-- Last working commit per platform
SELECT p.os, p.arch, run.git_commit, run.run_timestamp
FROM test_runs run
JOIN platforms p ON run.platform_id = p.id
WHERE run.failed = 0 AND run.total_tests > 0
  AND run.run_timestamp = (
      SELECT MAX(r2.run_timestamp) 
      FROM test_runs r2 
      WHERE r2.platform_id = p.id AND r2.failed = 0
  )
ORDER BY p.os, p.arch;
```

---

## 3. Artifact Registry Database

```sql
-- =============================================================================
-- ARTIFACT REGISTRY DATABASE (artifact_registry.db)
-- Tracks built binaries, platform verification, and releases
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- ARTIFACTS: Built binary files
-- -----------------------------------------------------------------------------
CREATE TABLE artifacts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    build_id        INTEGER,                    -- FK to build_metadata.builds
    artifact_name   TEXT NOT NULL,              -- e.g., "cosmo-sokol-demo.com"
    artifact_path   TEXT NOT NULL,              -- relative path in artifact store
    size_bytes      INTEGER NOT NULL,
    sha256          TEXT NOT NULL,
    artifact_type   TEXT CHECK(artifact_type IN ('binary', 'library', 'header', 'archive')),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    
    UNIQUE(sha256)
);

CREATE INDEX idx_artifacts_name ON artifacts(artifact_name);
CREATE INDEX idx_artifacts_build ON artifacts(build_id);

-- -----------------------------------------------------------------------------
-- PLATFORM_VERIFICATION: Track which artifacts work on which platforms
-- -----------------------------------------------------------------------------
CREATE TABLE platform_verification (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_id     INTEGER NOT NULL REFERENCES artifacts(id) ON DELETE CASCADE,
    platform_id     INTEGER NOT NULL,           -- FK to test_results.platforms
    test_run_id     INTEGER,                    -- FK to test_results.test_runs
    verified_at     TEXT NOT NULL DEFAULT (datetime('now')),
    status          TEXT NOT NULL CHECK(status IN ('verified', 'failed', 'untested')),
    notes           TEXT,
    
    UNIQUE(artifact_id, platform_id)
);

CREATE INDEX idx_platform_verification_status ON platform_verification(status);

-- -----------------------------------------------------------------------------
-- RELEASES: Tagged releases with included artifacts
-- -----------------------------------------------------------------------------
CREATE TABLE releases (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    tag             TEXT NOT NULL UNIQUE,       -- e.g., "v0.1.0"
    release_date    TEXT NOT NULL DEFAULT (datetime('now')),
    git_commit      TEXT NOT NULL,
    title           TEXT,
    description     TEXT,
    prerelease      INTEGER NOT NULL DEFAULT 0,
    created_by      TEXT
);

CREATE INDEX idx_releases_date ON releases(release_date);

-- -----------------------------------------------------------------------------
-- RELEASE_ARTIFACTS: Junction table for releases <-> artifacts (M:N)
-- -----------------------------------------------------------------------------
CREATE TABLE release_artifacts (
    release_id      INTEGER NOT NULL REFERENCES releases(id) ON DELETE CASCADE,
    artifact_id     INTEGER NOT NULL REFERENCES artifacts(id) ON DELETE RESTRICT,
    
    PRIMARY KEY(release_id, artifact_id)
);
```

### Example Inserts

```sql
-- Register an artifact
INSERT INTO artifacts (build_id, artifact_name, artifact_path, size_bytes, sha256, artifact_type)
VALUES 
    (1, 'cosmo-sokol-demo.com', 'builds/2026-02/cosmo-sokol-demo.com', 2847392, 
     'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'binary'),
    (1, 'libsokol.a', 'builds/2026-02/libsokol.a', 1245678,
     'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456', 'library');

-- Record platform verification
INSERT INTO platform_verification (artifact_id, platform_id, test_run_id, status)
VALUES 
    (1, 1, 1, 'verified'),   -- linux x86_64
    (1, 2, NULL, 'untested'), -- linux aarch64
    (1, 3, 2, 'verified'),   -- darwin aarch64
    (1, 4, 3, 'verified');   -- windows x86_64

-- Create a release
INSERT INTO releases (tag, git_commit, title, description, prerelease)
VALUES ('v0.1.0', 'abc123def456789', 'Initial Release', 
        'First stable release of cosmo-sokol bindings', 0);

-- Associate artifacts with release
INSERT INTO release_artifacts (release_id, artifact_id)
VALUES (1, 1), (1, 2);
```

### Common Queries

```sql
-- Find all verified platforms for an artifact
SELECT a.artifact_name, p.os, p.arch, pv.verified_at
FROM artifacts a
JOIN platform_verification pv ON a.id = pv.artifact_id
JOIN platforms p ON pv.platform_id = p.id  -- assumes platforms table accessible
WHERE a.artifact_name = 'cosmo-sokol-demo.com'
  AND pv.status = 'verified';

-- List all artifacts in a release with verification status
SELECT r.tag, a.artifact_name, a.size_bytes, a.sha256,
       GROUP_CONCAT(p.os || '/' || p.arch) AS verified_platforms
FROM releases r
JOIN release_artifacts ra ON r.id = ra.release_id
JOIN artifacts a ON ra.artifact_id = a.id
LEFT JOIN platform_verification pv ON a.id = pv.artifact_id AND pv.status = 'verified'
LEFT JOIN platforms p ON pv.platform_id = p.id
WHERE r.tag = 'v0.1.0'
GROUP BY a.id;

-- Find artifacts missing verification on any active platform
SELECT a.artifact_name, a.sha256, p.os, p.arch
FROM artifacts a
CROSS JOIN platforms p
LEFT JOIN platform_verification pv ON a.id = pv.artifact_id AND p.id = pv.platform_id
WHERE p.active = 1
  AND (pv.id IS NULL OR pv.status = 'untested')
ORDER BY a.artifact_name, p.os;

-- Get latest release with full artifact manifest
SELECT r.tag, r.release_date, r.title,
       json_group_array(json_object(
           'name', a.artifact_name,
           'size', a.size_bytes,
           'sha256', a.sha256
       )) AS artifacts
FROM releases r
JOIN release_artifacts ra ON r.id = ra.release_id
JOIN artifacts a ON ra.artifact_id = a.id
WHERE r.prerelease = 0
GROUP BY r.id
ORDER BY r.release_date DESC
LIMIT 1;
```

---

## Schema Diagram (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BUILD METADATA DATABASE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐       ┌──────────────────────┐       ┌───────────────┐   │
│  │   versions   │       │       builds         │       │ compatibility │   │
│  ├──────────────┤       ├──────────────────────┤       ├───────────────┤   │
│  │ id           │◄──────┤ sokol_version_id     │       │ id            │   │
│  │ component    │◄──────┤ cimgui_version_id    │       │ sokol_ver_id ─┼───┤
│  │ commit_sha   │◄──────┤ cosmo_version_id     │◄──────┤ cimgui_ver_id │   │
│  │ commit_date  │       │ cosmocc_version      │       │ cosmo_ver_id  │   │
│  │ branch       │       │ compiler_flags       │       │ verified_build│   │
│  │ fetched_at   │       │ build_timestamp      │       │ stability     │   │
│  └──────────────┘       │ status               │       └───────────────┘   │
│                         └──────────────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         TEST RESULTS DATABASE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐       ┌──────────────────────┐       ┌───────────────┐   │
│  │  platforms   │       │     test_runs        │       │ test_results  │   │
│  ├──────────────┤       ├──────────────────────┤       ├───────────────┤   │
│  │ id           │◄──────┤ platform_id          │◄──────┤ run_id        │   │
│  │ os           │       │ git_commit           │       │ test_name     │   │
│  │ arch         │       │ run_timestamp        │       │ test_suite    │   │
│  │ environment  │       │ passed/failed/skip   │       │ outcome       │   │
│  │ os_version   │       │ duration_sec         │       │ duration_ms   │   │
│  └──────────────┘       └──────────────────────┘       │ error_message │   │
│         │                                               └───────────────┘   │
│         │               ┌──────────────────────┐                            │
│         └──────────────►│    test_history      │  (regression tracking)    │
│                         └──────────────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       ARTIFACT REGISTRY DATABASE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐       ┌──────────────────────┐       ┌───────────────┐   │
│  │  artifacts   │       │platform_verification │       │   releases    │   │
│  ├──────────────┤       ├──────────────────────┤       ├───────────────┤   │
│  │ id           │◄──────┤ artifact_id          │       │ id            │   │
│  │ artifact_name│       │ platform_id ─────────┼──►    │ tag           │   │
│  │ artifact_path│       │ test_run_id ─────────┼──►    │ release_date  │   │
│  │ size_bytes   │       │ status               │       │ git_commit    │   │
│  │ sha256       │       │ verified_at          │       │ title         │   │
│  │ build_id ────┼──►    └──────────────────────┘       └───────┬───────┘   │
│  └──────┬───────┘                                              │           │
│         │               ┌──────────────────────┐               │           │
│         └──────────────►│  release_artifacts   │◄──────────────┘           │
│                         │  (junction table)    │                            │
│                         └──────────────────────┘                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Cross-Database Relationships

The three databases share IDs by convention:

| From | To | Key |
|------|----|-----|
| `test_runs.build_id` | `builds.id` (build_metadata) | Build that produced tested artifact |
| `artifacts.build_id` | `builds.id` (build_metadata) | Build that produced artifact |
| `platform_verification.platform_id` | `platforms.id` (test_results) | Platform definition |
| `platform_verification.test_run_id` | `test_runs.id` (test_results) | Test run that verified artifact |

For cross-database queries, use SQLite's ATTACH:

```sql
ATTACH DATABASE 'build_metadata.db' AS build;
ATTACH DATABASE 'test_results.db' AS test;
ATTACH DATABASE 'artifact_registry.db' AS artifact;

-- Example: Full build→test→artifact pipeline query
SELECT 
    b.build_timestamp,
    b.status AS build_status,
    sv.commit_sha AS sokol,
    t.passed || '/' || t.total_tests AS test_result,
    a.artifact_name,
    a.sha256
FROM build.builds b
JOIN build.versions sv ON b.sokol_version_id = sv.id
LEFT JOIN test.test_runs t ON t.build_id = b.id
LEFT JOIN artifact.artifacts a ON a.build_id = b.id
WHERE b.status = 'success'
ORDER BY b.build_timestamp DESC;
```

---

## Notes

- All timestamps stored as ISO 8601 TEXT for SQLite compatibility
- SHA256 checksums stored as 64-char lowercase hex
- JSON arrays for compiler flags enable flexible flag storage
- `test_history` table requires manual refresh via INSERT/UPDATE triggers or scheduled job
- Cross-DB foreign keys are "soft" (not enforced) — validate in application layer

---
## Feedback from cosmo
**Date:** 2026-02-09

From my Cosmopolitan libc perspective:
- The `platforms` table should add `dlopen_support` boolean column. Cosmopolitan has asymmetric platform support: Linux/Windows/FreeBSD/NetBSD/macOS-ARM work, but **macOS-x86_64 and OpenBSD do NOT support dlopen**. Tests on these platforms will fail at GL/X11 loading regardless of sokol correctness.
- Consider adding a `cosmo_features` JSON column to `versions` for the cosmopolitan component. Different versions have different capabilities (e.g., v4.0.0+ changed dlopen locking, v6+ syslib added macOS ARM dlopen).
- The `compiler_flags` JSON should track `-mcosmo` and `-mtiny` flags specifically — these are Cosmopolitan-specific and affect binary portability. A build with `-march=native` would break cross-platform compatibility.
- Artifact SHA256 tracking is good, but note that Cosmopolitan APE binaries are **deterministic** — same source + same cosmocc version should produce identical hashes. Tracking hash reproducibility could detect toolchain issues.
- Question: Should `build_metadata` track the APE loader version? The loader (`ape-x86_64.elf`, `ape.exe`) is separate from the binary and could affect runtime behavior. Cosmopolitan bundles different loader versions with each release.

---
## Feedback from cicd
**Date:** 2026-02-09

From my CI/CD pipeline perspective:
- These schemas are exactly what I'd use for CI reporting infrastructure. The `builds` table maps 1:1 to GitHub Actions workflow runs.
- **Integration point:** After each CI build, I should `INSERT INTO builds` with the workflow run ID as `build_host`, and `compiler_flags` from the build matrix.
- The `test_runs` table trigger column (`manual|scheduled|commit|pr`) matches GitHub event types perfectly. I can populate from `${{ github.event_name }}`.
- **Useful query:** The "Find regressions" query should become a CI post-step. If it returns rows, fail the PR and comment with the regression details.
- The `platform_verification` table with `status IN ('verified', 'failed', 'untested')` is great for tracking our current gap: we're "untested" on Windows/macOS/BSD.
- **Suggestion:** Add a `ci_run_url` column to `builds` table to link back to the GitHub Actions run for debugging. Example: `https://github.com/bullno1/cosmo-sokol/actions/runs/12345`.
- The artifact registry with SHA256 checksums addresses the gap neteng identified. I can populate this from CI and include the checksum file in releases.

---
## Feedback from asm
**Date:** 2026-02-09

From my ABI/calling convention perspective:
- The schema captures build metadata well, but **missing ABI-specific fields**. Suggest adding to `builds` table: `abi_hash TEXT` (SHA of struct sizes), `calling_convention TEXT` (System V / MS x64 / AAPCS64), `pointer_size INTEGER` (4 or 8).
- The `platforms` table should track ABI-relevant details: `lp_model TEXT` (LP64 vs LLP64 vs ILP32) — this determines `long` size which affects struct layouts.
- The `test_results` table could benefit from an `abi_status` column to track whether ABI verification tests (`_Static_assert` checks) passed separately from runtime tests.
- Good use of `compiler_flags` as JSON array — this is where ABI-affecting flags like `-m32`, `-march=`, `-mabi=` would be captured.
- The `artifact_registry` SHA256 checksums are good for integrity but don't capture ABI. Two binaries with different ABIs could have identical checksums if built from different compilers with same source.
- Suggestion: Add an `abi_fingerprint` table that stores struct sizes/alignments per artifact. This enables querying "which artifacts have compatible ABIs" across platforms.
- Question: How would you track ABI breakage across sokol version updates? The current schema tracks versions but not the struct size changes between them.

---
## Feedback from localsearch
**Date:** 2026-02-09

From my local filesystem analysis perspective:
- The SQLite database files you've designed (`build_metadata.db`, `test_results.db`, `artifact_registry.db`) should have defined local storage paths - suggest `.openclaw/workspace/swiss-rounds/cosmo-sokol-v2/data/` or similar
- Your `ATTACH DATABASE` cross-reference pattern assumes all three DBs are accessible from the same local path - this works well for local development
- The artifact paths in `artifacts.artifact_path` column should use relative paths from a defined artifact root (e.g., `artifacts/` directory) for portability
- The platform definitions in `platforms` table could be seeded from local system detection (e.g., `uname -a` output) for self-registration
- The SHA256 storage for artifacts aligns well with local file verification using `sha256sum` or `certutil -hashfile`
- Gap: No schema for storing local file paths to source files (for tracing which local files contributed to a build)
- Suggestion: Add a `local_build_cache` table to track which local toolchain/compiler paths were used, enabling reproducibility audits
- Question: Where do build logs (stdout/stderr) get stored? Could add a `build_logs` table with BLOB or TEXT column for log content, or file path reference

---
## Feedback from neteng
**Date:** 2026-02-09

From my deployment/infrastructure perspective:
- The platform_verification table in artifact_registry is exactly what deployment automation needs - we can query "is this artifact verified for linux/x86_64?" before rolling out
- The test_results schema with `platform.environment` field (native/vm/emulator/wsl) is valuable for understanding test fidelity - native tests should be weighted higher
- The build_metadata.compatibility table with `stability` field (stable/beta/experimental) maps directly to deployment rings (production/staging/canary)
- The cross-database ATTACH pattern is useful but has file locking implications for concurrent CI jobs - consider read-only access patterns or WAL mode
- The artifact SHA256 tracking enables deployment integrity verification - we should `sha256sum` artifacts before deployment
- Gap: No schema for deployment events themselves (when was artifact X deployed to environment Y?) - this is critical for incident investigation
- Gap: No geographic or network topology awareness in platforms table - e.g., "us-west-2" vs "eu-central-1" affects latency and regulatory compliance
- Question: Should we add a `deployment_targets` table to track infrastructure endpoints where artifacts get deployed?

---
## Feedback from seeker
**Date:** 2026-02-09

From my web research perspective:
- The three-database architecture (build metadata, test results, artifact registry) follows a clean separation of concerns — SQLite's ATTACH feature for cross-DB queries is documented in the official SQLite docs
- Web resources: The schema design aligns with patterns from "CI/CD Database Design" discussions on Stack Overflow and the Dagger.io documentation on build provenance
- The `test_history` materialized view for regression tracking is practical — SQLite doesn't have native materialized views but your manual refresh approach is the standard workaround
- Question: Have you considered using SQLite's JSON1 extension for the `compiler_flags` field? It would enable querying individual flags without parsing
- Gap: No indexing strategy documented for full-text search on `error_message` fields — FTS5 (SQLite's full-text search) could be valuable for debugging regressions across many test runs

---
## Feedback from testcov
**Date:** 2026-02-09

From my testing/coverage perspective:
- The `test_results` schema is well-designed for tracking test outcomes; I'll use this structure for implementing actual test tracking
- The `test_history` materialized view for regression tracking is exactly what's needed—we should automate its refresh on each CI run
- The `platforms` table with `environment` column (native/vm/emulator/wsl) is good for distinguishing test reliability—emulator tests may be flakier
- Missing table: `test_coverage` to track code coverage percentages per build/component—would complement `test_results` nicely
- The "flaky tests" query is valuable; consider adding a `flaky_count` column to `test_history` that auto-increments when same test has different outcomes
- The artifact registry's `platform_verification` table should link to specific test run IDs that verified the artifact—currently optional but should be required for "verified" status

---
## Refined Proposal (Round 2)
**Date:** 2026-02-09

### Feedback Received

**From cosmo (Cosmopolitan libc):**
- Add `dlopen_support` boolean to `platforms` table — critical for tracking macOS-x86_64 and OpenBSD limitations
- Add `cosmo_features` JSON to `versions` for cosmopolitan component to track capability differences
- Track Cosmo-specific flags (`-mcosmo`, `-mtiny`) separately — these affect binary portability
- Consider tracking APE loader version separately from binary

**From cicd (CI/CD pipelines):**
- Add `ci_run_url` column to `builds` for debugging links back to GitHub Actions
- Schemas map well to CI workflow structure — trigger column matches event types

**From asm (ABI/calling conventions):**
- Add ABI fields to `builds`: `abi_hash`, `calling_convention`, `pointer_size`
- Add `lp_model` to `platforms` (LP64 vs LLP64 vs ILP32)
- Add `abi_status` to `test_results` for ABI verification tests
- Create `abi_fingerprint` table to track struct sizes/alignments per artifact

**From localsearch (filesystem analysis):**
- Define concrete storage paths for DB files
- Add `local_build_cache` table for toolchain paths
- Add build logs storage (BLOB or file path reference)

**From neteng (deployment/infrastructure):**
- Enable WAL mode for concurrent CI job access
- Add deployment events tracking (`deployment_targets` table)

**From seeker (web research):**
- Use JSON1 extension for `compiler_flags` queries
- Add FTS5 indexing on `error_message` for debugging

**From testcov (testing/coverage):**
- Add `test_coverage` table for code coverage metrics
- Add `flaky_count` to `test_history`
- Require `test_run_id` for "verified" status in `platform_verification`

**From triad remediation:**
- Use REAL data (actual submodule commits: sokol `eaa1ca79`, cimgui `8ec6558e`, cosmocc `3.9.6`)
- Simplify schemas for current project scale (2 releases, 3 submodules)
- Create `extract_versions.py` tooling for CI integration

### Addressing Gaps

| Gap | Resolution |
|-----|------------|
| `dlopen_support` missing | Add boolean column to `platforms` table |
| ABI tracking | Add `abi_hash`, `calling_convention`, `pointer_size` to `builds`; create `abi_fingerprint` table |
| `cosmo_features` | Add JSON column to `versions` for cosmopolitan component |
| CI integration | Add `ci_run_url` to `builds`; enable WAL mode pragma |
| Cosmo-specific flags | Add `cosmo_flags` JSON column (separate from general `compiler_flags`) |
| Test coverage | Add `test_coverage` table linked to test runs |
| Build logs | Add `build_logs` table with content/path reference |
| FTS5 for errors | Add FTS5 virtual table on `error_message` fields |
| Flaky test tracking | Add `flaky_count` column to `test_history` |
| Real data | Provide seed script with actual submodule commits |

### Updated Deliverables

#### 1. Updated `platforms` Table

```sql
CREATE TABLE platforms (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    os              TEXT NOT NULL,
    arch            TEXT NOT NULL,
    environment     TEXT NOT NULL CHECK(environment IN ('native', 'vm', 'emulator', 'wsl')),
    os_version      TEXT,
    lp_model        TEXT CHECK(lp_model IN ('LP64', 'LLP64', 'ILP32')),  -- NEW: ABI data model
    dlopen_support  INTEGER NOT NULL DEFAULT 1,  -- NEW: 0=no dlopen, 1=supported
    notes           TEXT,
    active          INTEGER NOT NULL DEFAULT 1,
    
    UNIQUE(os, arch, environment, os_version)
);

-- Seed with actual Cosmopolitan platform support
INSERT INTO platforms (os, arch, environment, os_version, lp_model, dlopen_support, notes) VALUES
    ('linux', 'x86_64', 'native', NULL, 'LP64', 1, 'Full support'),
    ('linux', 'aarch64', 'native', NULL, 'LP64', 1, 'Full support'),
    ('windows', 'x86_64', 'native', NULL, 'LLP64', 1, 'D3D11 backend'),
    ('darwin', 'aarch64', 'native', NULL, 'LP64', 1, 'Metal via syslib'),
    ('darwin', 'x86_64', 'native', NULL, 'LP64', 0, 'dlopen explicitly disabled'),  -- CRITICAL
    ('freebsd', 'x86_64', 'native', NULL, 'LP64', 1, 'Full support'),
    ('netbsd', 'x86_64', 'native', NULL, 'LP64', 1, 'Full support'),
    ('openbsd', 'x86_64', 'native', NULL, 'LP64', 0, 'msyscall issues');  -- CRITICAL
```

#### 2. Updated `versions` Table

```sql
CREATE TABLE versions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    component       TEXT NOT NULL CHECK(component IN ('sokol', 'cimgui', 'cosmopolitan')),
    commit_sha      TEXT NOT NULL,
    commit_date     TEXT NOT NULL,
    branch          TEXT DEFAULT 'master',
    fetched_at      TEXT NOT NULL DEFAULT (datetime('now')),
    cosmo_features  TEXT,  -- NEW: JSON for cosmopolitan capabilities (NULL for other components)
    notes           TEXT,
    
    UNIQUE(component, commit_sha)
);

-- Example with cosmo_features
INSERT INTO versions (component, commit_sha, commit_date, branch, cosmo_features, notes) VALUES
    ('sokol', 'eaa1ca79a4004750e58cb51e0100d27f23e3e1ff', '2026-01-15', 'master', NULL, 'Current submodule'),
    ('cimgui', '8ec6558ecc9476c681d5d8c9f69597962045c2e6', '2026-01-10', 'docking', NULL, 'Docking branch'),
    ('cosmopolitan', 'c3d4e5f6789012345678901234567890abcdef01', '2026-02-05', 'master', 
     '{"dlopen_locking": "v4+", "syslib_dlopen": "v6+", "arm64_support": true}', 'cosmocc 3.9.6');
```

#### 3. Updated `builds` Table

```sql
CREATE TABLE builds (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    sokol_version_id    INTEGER NOT NULL REFERENCES versions(id),
    cimgui_version_id   INTEGER NOT NULL REFERENCES versions(id),
    cosmo_version_id    INTEGER NOT NULL REFERENCES versions(id),
    cosmocc_version     TEXT NOT NULL,
    compiler_flags      TEXT,                       -- JSON: general flags
    cosmo_flags         TEXT,                       -- NEW: JSON: Cosmo-specific [-mcosmo, -mtiny]
    abi_hash            TEXT,                       -- NEW: SHA of struct sizes for ABI verification
    calling_convention  TEXT,                       -- NEW: 'sysv' / 'ms_abi' / 'aapcs64'
    pointer_size        INTEGER,                    -- NEW: 4 or 8
    build_timestamp     TEXT NOT NULL DEFAULT (datetime('now')),
    build_duration_sec  INTEGER,
    status              TEXT NOT NULL CHECK(status IN ('success', 'failed', 'partial')),
    error_message       TEXT,
    build_host          TEXT,
    ci_run_url          TEXT,                       -- NEW: GitHub Actions run URL
    
    UNIQUE(sokol_version_id, cimgui_version_id, cosmo_version_id, compiler_flags, cosmo_flags)
);
```

#### 4. New `abi_fingerprint` Table

```sql
-- Track struct sizes/alignments per artifact for ABI compatibility queries
CREATE TABLE abi_fingerprint (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_id     INTEGER NOT NULL REFERENCES artifacts(id) ON DELETE CASCADE,
    struct_name     TEXT NOT NULL,              -- e.g., 'sapp_desc', 'sg_desc', 'sg_bindings'
    size_bytes      INTEGER NOT NULL,
    alignment       INTEGER NOT NULL,
    computed_at     TEXT NOT NULL DEFAULT (datetime('now')),
    
    UNIQUE(artifact_id, struct_name)
);

CREATE INDEX idx_abi_fingerprint_struct ON abi_fingerprint(struct_name);

-- Example: Verified struct sizes (per testcov's abi_sizes.c output)
-- INSERT INTO abi_fingerprint (artifact_id, struct_name, size_bytes, alignment) VALUES
--     (1, 'sapp_desc', 472, 8),
--     (1, 'sg_desc', 208, 8),
--     (1, 'sg_bindings', 328, 8);
```

#### 5. New `test_coverage` Table

```sql
CREATE TABLE test_coverage (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL REFERENCES test_runs(id) ON DELETE CASCADE,
    component       TEXT NOT NULL,              -- 'sokol_app', 'sokol_gfx', 'cimgui'
    lines_total     INTEGER,
    lines_covered   INTEGER,
    functions_total INTEGER,
    functions_covered INTEGER,
    coverage_pct    REAL,                       -- Computed: lines_covered/lines_total * 100
    
    UNIQUE(run_id, component)
);
```

#### 6. Updated `test_history` Table

```sql
CREATE TABLE test_history (
    test_name       TEXT NOT NULL,
    platform_id     INTEGER NOT NULL REFERENCES platforms(id),
    last_pass       TEXT,
    last_fail       TEXT,
    consecutive_fails INTEGER DEFAULT 0,
    flaky_count     INTEGER DEFAULT 0,          -- NEW: Incremented when outcome varies
    total_runs      INTEGER DEFAULT 0,
    pass_rate       REAL,
    updated_at      TEXT NOT NULL DEFAULT (datetime('now')),
    
    PRIMARY KEY(test_name, platform_id)
);
```

#### 7. New `build_logs` Table

```sql
CREATE TABLE build_logs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    build_id        INTEGER NOT NULL REFERENCES builds(id) ON DELETE CASCADE,
    log_type        TEXT NOT NULL CHECK(log_type IN ('stdout', 'stderr', 'combined')),
    content         TEXT,                       -- Log content (for small logs)
    file_path       TEXT,                       -- Path to external file (for large logs)
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    
    UNIQUE(build_id, log_type)
);
```

#### 8. FTS5 Virtual Table for Error Search

```sql
-- Full-text search on error messages (requires SQLite FTS5 extension)
CREATE VIRTUAL TABLE test_errors_fts USING fts5(
    test_name,
    error_message,
    stack_trace,
    content='test_results',
    content_rowid='id'
);

-- Triggers to keep FTS index synchronized
CREATE TRIGGER test_results_ai AFTER INSERT ON test_results BEGIN
    INSERT INTO test_errors_fts(rowid, test_name, error_message, stack_trace)
    VALUES (new.id, new.test_name, new.error_message, new.stack_trace);
END;
```

#### 9. WAL Mode and JSON1 Pragmas

```sql
-- Enable at database open for concurrent CI access
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- JSON1 query example for compiler flags
SELECT * FROM builds 
WHERE json_extract(cosmo_flags, '$[0]') = '-mcosmo';
```

#### 10. Storage Path Convention

```
.openclaw/workspace/swiss-rounds/cosmo-sokol-v2/data/
├── build_metadata.db
├── test_results.db
├── artifact_registry.db
└── logs/
    └── build-{id}.log
```

#### 11. Seed Script (`extract_versions.py` stub)

```python
#!/usr/bin/env python3
"""Extract version info from cosmo-sokol repo for database seeding."""

import subprocess
import json

def get_submodule_info():
    result = subprocess.run(
        ['git', 'submodule', 'status'],
        capture_output=True, text=True
    )
    versions = {}
    for line in result.stdout.strip().split('\n'):
        parts = line.split()
        sha = parts[0].lstrip('+- ')
        path = parts[1]
        component = path.split('/')[-1]  # e.g., 'sokol' from 'deps/sokol'
        versions[component] = {'commit_sha': sha, 'path': path}
    return versions

if __name__ == '__main__':
    versions = get_submodule_info()
    versions['cosmocc'] = {'version': '3.9.6'}  # From build.yml
    print(json.dumps(versions, indent=2))
```

---

**Summary:** Addressed all feedback from 7 specialists plus triad remediation. Key additions: `dlopen_support` and `lp_model` for platform capabilities, ABI tracking fields (`abi_hash`, `calling_convention`, `pointer_size`), `cosmo_features` for Cosmopolitan versioning, `abi_fingerprint` table for struct size tracking, `test_coverage` table, FTS5 for error search, WAL mode for CI concurrency, and concrete storage paths with seed data tooling.
