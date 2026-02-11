# Aider Source Manifest

Generated: 2026-02-11
Source: https://github.com/Aider-AI/aider @ main

## Overview

Aider is an AI pair programming CLI that integrates with git repos and supports multiple LLM backends via LiteLLM. It provides rapid feedback through auto-commits, linting, testing, and repo-map context.

## Core Architecture

### Entry Point
| Name | File | Purpose |
|------|------|---------|
| `main()` | `aider/main.py` | CLI entry, config loading, Coder initialization |
| `get_parser()` | `aider/args.py` | ConfigArgParse setup with all CLI flags |

### Coder (The Heart)
| Name | Signature | File | Purpose |
|------|-----------|------|---------|
| `Coder.create()` | `(main_model, edit_format, io, from_coder, **kwargs) -> Coder` | `aider/coders/base_coder.py` | Factory method - creates appropriate coder |
| `Coder.__init__()` | `(main_model, io, repo, fnames, ...)` | `aider/coders/base_coder.py` | Initialize with model, IO, git repo, files |
| `Coder.clone()` | `(**kwargs) -> Coder` | `aider/coders/base_coder.py` | Create new coder from existing |
| `Coder.run()` | `(message) -> str` | `aider/coders/base_coder.py` | Run a coding turn |

### Key Coder Attributes
| Attribute | Type | Purpose |
|-----------|------|---------|
| `abs_fnames` | `set[str]` | Editable files (absolute paths) |
| `abs_read_only_fnames` | `set[str]` | Read-only context files |
| `repo` | `GitRepo` | Git integration |
| `repo_map` | `RepoMap` | Token-limited repo context |
| `main_model` | `Model` | Active LLM |
| `edit_format` | `str` | Edit format (diff, whole, udiff, architect, ask) |
| `auto_commits` | `bool` | Auto-commit after edits |
| `auto_lint` | `bool` | Auto-lint after edits |
| `auto_test` | `bool` | Auto-test after edits |
| `stream` | `bool` | Stream responses |
| `done_messages` | `list[dict]` | Completed conversation history |
| `cur_messages` | `list[dict]` | Current turn messages |

### Commands (Interactive)
| Name | Signature | File | Purpose |
|------|-----------|------|---------|
| `Commands.cmd_add()` | `(args)` | `aider/commands.py` | `/add` - add files to chat |
| `Commands.cmd_drop()` | `(args)` | `aider/commands.py` | `/drop` - remove files from chat |
| `Commands.cmd_model()` | `(args)` | `aider/commands.py` | `/model` - switch main model |
| `Commands.cmd_chat_mode()` | `(args)` | `aider/commands.py` | `/chat-mode` - switch edit format |
| `Commands.cmd_commit()` | `(args)` | `aider/commands.py` | `/commit` - manual commit |
| `Commands.cmd_lint()` | `(args)` | `aider/commands.py` | `/lint` - lint and fix |
| `Commands.cmd_web()` | `(args)` | `aider/commands.py` | `/web` - scrape URL to chat |
| `Commands.cmd_clear()` | `(args)` | `aider/commands.py` | `/clear` - clear history |
| `Commands.cmd_reset()` | `(args)` | `aider/commands.py` | `/reset` - clear history + files |
| `Commands.cmd_run()` | `(args)` | `aider/commands.py` | `!cmd` - run shell command |

### Edit Formats (Coder Subclasses)
| Format | File | Description |
|--------|------|-------------|
| `diff` | `aider/coders/editblock_coder.py` | Search/replace blocks |
| `whole` | `aider/coders/wholefile_coder.py` | Full file replacement |
| `udiff` | `aider/coders/udiff_coder.py` | Unified diff patches |
| `architect` | `aider/coders/architect_coder.py` | Two-model: architect designs, editor implements |
| `ask` | `aider/coders/ask_coder.py` | Q&A only, no edits |

### Git Integration
| Name | Signature | File | Purpose |
|------|-----------|------|---------|
| `GitRepo.__init__()` | `(io, fnames, git_dname, models)` | `aider/repo.py` | Initialize git repo wrapper |
| `GitRepo.commit()` | `(message, coder)` | `aider/repo.py` | Commit with optional AI message |
| `GitRepo.is_dirty()` | `() -> bool` | `aider/repo.py` | Check for uncommitted changes |
| `GitRepo.get_dirty_files()` | `() -> list[str]` | `aider/repo.py` | List modified files |

### RepoMap (Context Management)
| Name | Signature | File | Purpose |
|------|-----------|------|---------|
| `RepoMap.__init__()` | `(root, io, main_model, ...)` | `aider/repomap.py` | Initialize repo mapper |
| `RepoMap.get_repo_map()` | `(fnames, other_fnames) -> str` | `aider/repomap.py` | Generate token-limited repo map |

### Linter Integration
| Name | Signature | File | Purpose |
|------|-----------|------|---------|
| `Linter.__init__()` | `(encoding, root, ...)` | `aider/linter.py` | Initialize linter |
| `Linter.lint()` | `(fname) -> str` | `aider/linter.py` | Run lint, return errors |

## Key CLI Arguments

### Model Selection
```
--model MODEL           Main chat model
--weak-model MODEL      Commit/summary model  
--editor-model MODEL    Architect editor model
--edit-format FORMAT    diff|whole|udiff|architect|ask
```

### Git Behavior
```
--auto-commits          Auto-commit LLM changes (default: True)
--dirty-commits         Commit when repo dirty (default: True)
--dry-run               No file modifications
```

### Feedback Loop
```
--auto-lint             Lint after changes (default: True)
--auto-test             Test after changes (default: False)
--lint-cmd "lang: cmd"  Custom lint command
--test-cmd "cmd"        Test command
--watch-files           Watch for ai coding comments
```

### Context
```
--map-tokens N          Repo map token budget (default: 1024)
--map-refresh MODE      auto|always|files|manual
FILES                   Files to add to chat (positional)
--read FILE             Add read-only file
```

### Cache & Performance
```
--cache-prompts         Enable prompt caching
--stream/--no-stream    Streaming responses
```

## Rapid Feedback Features (Spark Equivalent)

1. **Auto-lint**: `--auto-lint` runs linter after every edit, feeds errors back
2. **Auto-test**: `--auto-test` runs tests, feeds failures back
3. **Watch mode**: `--watch-files` monitors for `# ai:` comments, triggers edits
4. **Repo map**: Automatic context from repository structure
5. **Git integration**: Every successful edit = immediate commit

## What Does NOT Exist

- ❌ `--compile` flag — No built-in compile step (use `--lint-cmd` with a compiler)
- ❌ Native ASM/C awareness — Uses tree-sitter, but no deep ASM understanding
- ❌ Type feedback loop — No TypeScript-style type checking integration
- ❌ REPL mode — No interactive language REPL integration
- ❌ `run_and_observe()` — No built-in "run code, capture output, iterate" loop
- ❌ GPU acceleration — Pure Python, no GPU features

## Integration Pattern for C/ASM Rapid Feedback

To achieve Spark-like feedback for C/ASM with Aider:

```bash
# Set up lint command for C
aider --lint-cmd "c: clang -fsyntax-only -Wall -Wextra" \
      --auto-lint \
      --test-cmd "make test" \
      --auto-test \
      src/*.c

# Or for assembly
aider --lint-cmd "asm: nasm -f elf64 -w+all" \
      --auto-lint \
      src/*.asm
```

## Installation

```bash
pip install aider-chat
# or
pipx install aider-chat
```

## Configuration Files

- `.aider.conf.yml` — YAML config in repo root
- `~/.aider.conf.yml` — Global config
- `.aiderignore` — Files to exclude (gitignore syntax)
- `.aider.model.settings.yml` — Custom model configs

---

*This manifest is ground truth. Before using any aider feature, verify it exists here.*
