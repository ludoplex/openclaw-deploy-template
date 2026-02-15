# Windows 11 GUI Automation Skill

## Overview
Automated GUI interaction for Windows 11 from WSL2/OpenClaw. Includes verified click coordinates for common dialogs, danger zone avoidance, and recovery procedures.

## Quick Start
```powershell
# Import the module
Import-Module "C:\Users\user\.openclaw\workspace\skills\win11-gui-automation\Win11GuiAuto.psm1"

# Click Claude Code input (verified safe)
Invoke-ClaudeInputClick -LeftBias

# Click using verified ID
Invoke-SafeClick -Id "claude-input-center"

# Check if coords are dangerous
Test-InDangerZone -X 1900 -Y 30
```

## Screen Configuration (Verified)
- **Resolution:** 1920x1080
- **Working Area:** 1920x1032 (taskbar: 48px bottom)
- **DPI:** Standard (100%)

---

## VERIFIED CLICK COORDINATES

### Claude Code Desktop
**Window typical position:** (139, 60) to (1139, 851)  
**Window size:** 1000x791

| Target | Absolute Coords | Relative Position | Status |
|--------|-----------------|-------------------|--------|
| **Input Area (SAFE)** | **(639, 751)** | Center-X, 87% down | ✅ VERIFIED WORKING |
| Input Area (LEFT safe) | (489, 693) | 35% from left, 80% down | ✅ VERIFIED WORKING |
| Input Area (safe spread) | (481, 691) | Slightly left of above | ✅ VERIFIED WORKING |

**DANGER ZONES (Claude Code):**
- Bottom-right quadrant: (800+, 700+) - Stop/Cancel buttons
- Top-right: (1050+, 60-100) - Window close X
- Right edge: (1100+, any) - Scrollbar/close

---

### Windows 11 UAC/Consent Dialogs
**Typical dialog size:** ~500x350 centered on screen  
**Center of 1920x1080:** (960, 540)

| Dialog Type | OK/Yes Button | Cancel/No Button | Notes |
|-------------|---------------|------------------|-------|
| UAC Prompt | **(885, 590)** | (1035, 590) | Yes left, No right |
| Standard Consent | **(860, 580)** | (1060, 580) | OK left, Cancel right |
| Admin Elevation | **(885, 595)** | (1035, 595) | Continue/Cancel |
| SmartScreen | **(820, 550)** | (1100, 550) | Run Anyway / Don't Run |

**UAC Safe Click Formula (1920x1080):**
```
OK/Yes button: X = 960 - 75 = 885, Y = 540 + 50 = 590
              Coords: (885, 590)
```

---

### Common Windows Dialogs

| Dialog | OK/Confirm | Cancel/Close | Size |
|--------|------------|--------------|------|
| MessageBox (centered) | (910, 565) | (1010, 565) | ~300x150 |
| File Picker | (1650, 980) | (1780, 980) | Large |
| Save Dialog | (1680, 985) | (1800, 985) | Large |
| Properties | (780, 680) | (880, 680) | ~400x500 |
| Settings flyout | Varies | Top-right X | Varies |

---

## DANGER ZONES (Global)

```
Screen Layout (1920x1080):
┌────────────────────────────────────────────────────────╳─┐
│ Title bar - DRAG ZONE - avoid clicking                 X │ 0-40px
├──────────────────────────────────────────────────────────┤
│                                                          │
│                    SAFE ZONE                             │
│                    (most of screen)                      │
│                                                          │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                                    │ CANCEL ZONE │███████│ 
│  OK/YES typically here ──────────►│◄────────────│███████│ Bottom-right
└────────────────────────────────────────────────▒▒▒▒▒▒▒▒▒─┘
                                                 └─ Taskbar (1032-1080)
```

**Always avoid:**
- X > 1800, Y < 50 (window close)
- X > 1750, Y > 900 (dialog Cancel buttons)
- Y > 1032 (taskbar)
- Y < 40 (title bars)

---

## Scripts Reference

Located at: `C:\Users\user\.openclaw\workspace\scripts\contingency\`

| Script | Purpose | Key Params |
|--------|---------|------------|
| `safe-click.ps1` | Click avoiding danger zones | -WindowTitle, -Clicks |
| `smart-click.ps1` | ML-style spread pattern | -TargetArea, -SpreadPx |
| `battleship-click.ps1` | Checkerboard hunt pattern | -CenterX, -CenterY |
| `type-text.ps1` | Type into focused window | -Text, -Enter |
| `auto-recover.ps1` | Full OpenClaw recovery | -DryRun, -Force |
| `gui-interact.ps1` | Claude Code interaction | -Action |

---

## Usage Examples

### Click Claude Code Input (Safe)
```powershell
# Absolute coordinates (verified)
& safe-click.ps1 -WindowTitle "Claude" -Clicks 1

# Then type
& type-text.ps1 -Text "Hello" -Enter
```

### Click UAC "Yes" Button
```powershell
# Direct click at verified UAC Yes position
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Click {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, int e);
}
"@
[Click]::SetCursorPos(885, 590)
Start-Sleep -Milliseconds 100
[Click]::mouse_event(0x0002, 0, 0, 0, 0)  # Down
[Click]::mouse_event(0x0004, 0, 0, 0, 0)  # Up
```

### Safe Dialog Automation Pattern
```powershell
# 1. Find dialog
$dialog = Get-Process | Where-Object { $_.MainWindowTitle -match "consent|UAC|User Account" }

# 2. Calculate OK button (left of center, bottom third)
$okX = $dialogCenterX - 75
$okY = $dialogCenterY + 50

# 3. Click
[Click]::SetCursorPos($okX, $okY)
```

---

## Coordinate Discovery Process

When encountering a new dialog:

1. **Capture bounds:**
```powershell
$proc = Get-Process | Where-Object { $_.MainWindowTitle -like "*DialogName*" }
# Use GetWindowRect to find position
```

2. **Calculate button positions:**
   - OK/Yes: Usually 40% from center-left, bottom third
   - Cancel/No: Usually 40% from center-right, bottom third

3. **Test with DryRun first:**
```powershell
& battleship-click.ps1 -CenterX $estX -CenterY $estY -Spread 20 -DryRun
```

4. **Verify and record** coordinates in this file.

---

## Recovery Coordinates Log

| Date | Dialog/Window | Action | Coords | Result |
|------|---------------|--------|--------|--------|
| 2026-02-14 | Claude Code Input | Click | (639, 751) | ✅ SUCCESS |
| 2026-02-14 | Claude Code Input | Safe Click | (489, 693) | ✅ SUCCESS |
| 2026-02-14 | Claude Code Input | Safe Click | (481, 691) | ✅ SUCCESS |

---

## Troubleshooting

**Click not registering:**
- Window may not be focused - call SetForegroundWindow first
- Coordinates may be off due to DPI scaling
- Dialog may have moved - recalculate bounds

**Clicking wrong button:**
- Check if dialog is actually centered
- Verify screen resolution hasn't changed
- Use DryRun to preview coordinates

**UAC not accessible:**
- UAC runs on secure desktop - standard automation may not work
- May need to disable secure desktop or use other methods
