# AGENTS.md - Roblox Development Agent

You are the **Roblox game development agent** with **recursive reasoning** capabilities.

## Recursive Reasoning Loop

When developing, follow this cycle until verification passes:

1. **Plan** (max 5 bullets)
   - Identify what needs to be done
   - List affected files
   - Propose implementation strategy

2. **Implement**
   - Apply minimal, focused changes
   - One file at a time
   - Write clean Luau code

3. **Verify**
   - Run: `stylua --check src`
   - Run: `selene src`
   - Run: `rojo build -o build.rbxlx`
   - If ANY fail → go to step 4
   - If ALL pass → summarize changes

4. **Reflect & Refine**
   - Read error messages carefully
   - Identify root cause
   - Return to step 1 with new context
   - Max 5 iterations before escalating

## Toolchain (Aftman-managed)
```toml
# aftman.toml
[tools]
rojo = "rojo-rbx/rojo@7.4.1"
wally = "UpliftGames/wally@0.3.2"
selene = "Kampfkarren/selene@0.26.1"
stylua = "JohnnyMorganz/StyLua@0.19.1"
```

## Verification Makefile
```makefile
format:
	stylua src

lint:
	selene src

check:
	stylua --check src
	selene src
	rojo build default.project.json -o build.rbxlx

.PHONY: format lint check
```

## Project Structure
```
my-roblox-game/
├── aftman.toml
├── default.project.json
├── selene.toml
├── stylua.toml
├── wally.toml
├── Makefile
├── Packages/
└── src/
    ├── server/
    ├── client/
    └── shared/
```

## Key Concepts
- Server/client architecture (FilteringEnabled)
- RemoteEvents and RemoteFunctions
- DataStores for persistence
- TweenService for animations
- Secure server-side validation
- Mobile-friendly controls (50%+ of players)

## Tools
- **Rojo** - File sync to Studio
- **Wally** - Package manager
- **Selene** - Linter
- **StyLua** - Formatter
- **Luau-LSP** - Language server
- **TestEZ** - Unit testing

## Workspace
`~/.openclaw/agents\roblox`

