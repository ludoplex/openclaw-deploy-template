# roblox-verify

Recursive verification hook for Roblox projects. Runs the verification loop (lint, format check, build) and iterates on failures.

## Events
- `command:roblox:verify` - Manual trigger
- `file:changed` - Auto-trigger on .lua/.luau changes (when watching)

## Requirements
- Aftman-managed toolchain (rojo, selene, stylua)
- Makefile with `check` target in project root
- Project structure: `src/server`, `src/client`, `src/shared`

## Config
```json
{
  "maxIterations": 5,
  "verifyCommands": ["stylua --check src", "selene src", "rojo build -o build.rbxlx"]
}
```

## Usage
From the roblox agent, run:
```
make check
```

Or trigger the full recursive loop by describing the task and letting the agent iterate.
