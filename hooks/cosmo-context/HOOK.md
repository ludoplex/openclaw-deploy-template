# Cosmo Context Hook

Injects Cosmopolitan Libc conventions, APE tooling knowledge, and ecosystem resources into the cosmo agent context.

## Triggers
- Always (on session start)

## Purpose
Ensures the cosmo agent:
1. Uses native Cosmopolitan APIs and conventions (NO WSL/emulation)
2. Has complete knowledge of APE tools and repos
3. Understands transpilation options (Python, Rust, Nim, etc.)
4. Knows Sokol + Cosmo integration patterns
