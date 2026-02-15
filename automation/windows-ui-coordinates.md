# Windows 11 Native UI Automation Coordinates

**Screen Resolution:** 1920x1080 (adjust proportionally for other resolutions)
**Purpose:** Quick mouse automation for features lacking good CLI/API alternatives

---

## UAC Consent Dialog
**Launch:** Triggered by elevation requests
**Position:** Centered on screen

| Element | X | Y | Notes |
|---------|---|---|-------|
| Yes button | 870 | 655 | Left button of pair |
| No button | 1050 | 655 | Right button of pair |
| Show details | 960 | 580 | Expands dialog |

**CLI Alternative:** Run from elevated context, or use Task Scheduler with HIGHEST privilege

---

## Windows Security (Defender)
**Launch:** `start windowsdefender:`

| Element | X | Y | Notes |
|---------|---|---|-------|
| Virus & threat protection | 250 | 200 | Left nav |
| Firewall & network | 250 | 280 | Left nav |
| Quick scan button | 400 | 350 | After selecting V&T protection |
| Scan options | 400 | 420 | Full/Custom scan |
| Real-time protection toggle | 750 | 380 | In V&T settings |

**CLI Alternative:** `Get-MpComputerStatus`, `Start-MpScan`, but some toggles GUI-only

---

## Task Manager
**Launch:** `taskmgr` or Ctrl+Shift+Esc

| Element | X | Y | Notes |
|---------|---|---|-------|
| Processes tab | 100 | 60 | Top tabs |
| Performance tab | 200 | 60 | |
| Startup tab | 400 | 60 | Manage startup apps |
| End task button | 1800 | 950 | Bottom right |
| More details | 960 | 400 | If in compact mode |
| Run new task | 100 | 100 | File menu area |

**CLI Alternative:** `Get-Process`, `Stop-Process`, but startup management easier via GUI

---

## Sound Settings (Volume Mixer)
**Launch:** `sndvol` (mixer) or `mmsys.cpl` (full settings)

| Element | X | Y | Notes |
|---------|---|---|-------|
| Output device dropdown | 960 | 150 | Top of Settings > Sound |
| Input device dropdown | 960 | 400 | |
| Volume slider | 960 | 250 | Main volume |
| App volume (first) | 200 | 300 | In sndvol |

**CLI Alternative:** `Set-AudioDevice` (requires module), or nircmd

---

## Display Settings
**Launch:** `ms-settings:display` or `desk.cpl`

| Element | X | Y | Notes |
|---------|---|---|-------|
| Scale dropdown | 1200 | 400 | 100%, 125%, etc. |
| Resolution dropdown | 1200 | 500 | |
| Multiple displays | 1200 | 300 | Extend/Duplicate |
| Night light toggle | 1400 | 250 | |
| Identify button | 800 | 200 | Shows monitor numbers |

**CLI Alternative:** `displayswitch.exe /extend`, but scaling is GUI-only

---

## Network Connections
**Launch:** `ncpa.cpl`

| Element | X | Y | Notes |
|---------|---|---|-------|
| First adapter | 150 | 150 | Icon grid |
| Right-click context | +10 | +10 | After positioning |
| Properties (in menu) | +50 | +120 | From right-click |
| Disable (in menu) | +50 | +80 | |

**CLI Alternative:** `netsh`, `Get-NetAdapter`, `Disable-NetAdapter`

---

## Credential Manager
**Launch:** `control keymgr.dll` or `rundll32.exe keymgr.dll,KRShowKeyMgr`

| Element | X | Y | Notes |
|---------|---|---|-------|
| Windows Credentials | 300 | 200 | Tab/section |
| Web Credentials | 500 | 200 | |
| Add Windows credential | 300 | 500 | |
| First credential expand | 400 | 280 | Arrow to show details |
| Remove link | 600 | 350 | After expanding |

**CLI Alternative:** `cmdkey /list`, `cmdkey /add`, `cmdkey /delete`

---

## Bluetooth & Devices
**Launch:** `ms-settings:bluetooth`

| Element | X | Y | Notes |
|---------|---|---|-------|
| Bluetooth toggle | 1400 | 150 | On/off |
| Add device button | 400 | 250 | + Add device |
| First paired device | 400 | 350 | |
| Device options (⋮) | 1500 | 350 | Three dots menu |
| Remove device | 1500 | 420 | In dropdown |

**CLI Alternative:** Limited - `btpair.exe` for pairing, but discovery is GUI

---

## Windows Update
**Launch:** `ms-settings:windowsupdate`

| Element | X | Y | Notes |
|---------|---|---|-------|
| Check for updates | 400 | 200 | Main button |
| Download & install | 400 | 300 | When updates available |
| Restart now | 400 | 350 | After download |
| Pause updates | 400 | 450 | |
| Update history | 400 | 500 | |

**CLI Alternative:** `UsoClient StartScan`, Windows Update PowerShell module

---

## Services (services.msc)
**Launch:** `services.msc`

| Element | X | Y | Notes |
|---------|---|---|-------|
| Service list start | 400 | 150 | First service row |
| Start button | 100 | 80 | Toolbar |
| Stop button | 130 | 80 | |
| Restart button | 160 | 80 | |
| Properties (dbl-click) | - | - | Double-click service |

**CLI Alternative:** `sc start/stop`, `Start-Service`, `Stop-Service` — prefer CLI

---

## Device Manager
**Launch:** `devmgmt.msc`

| Element | X | Y | Notes |
|---------|---|---|-------|
| First category | 150 | 100 | Tree view |
| Scan for changes | 500 | 60 | Toolbar icon |
| Action menu | 50 | 30 | Menu bar |
| Right-click context | +10 | +10 | On selected device |

**CLI Alternative:** `pnputil`, `Get-PnpDevice`, but driver updates often need GUI

---

## Certificate Manager
**Launch:** `certmgr.msc` (user) or `certlm.msc` (local machine, needs admin)

| Element | X | Y | Notes |
|---------|---|---|-------|
| Personal | 150 | 100 | Left tree |
| Trusted Root CAs | 150 | 150 | |
| Certificate list | 500 | 150 | Right pane |
| Import wizard | Action menu | | |

**CLI Alternative:** `certutil`, `Import-Certificate` — prefer CLI for automation

---

## Disk Management
**Launch:** `diskmgmt.msc`

| Element | X | Y | Notes |
|---------|---|---|-------|
| Disk 0 | 150 | 400 | Bottom pane |
| Volume list | 500 | 150 | Top pane |
| Right-click for actions | +10 | +10 | Context menus |

**CLI Alternative:** `diskpart`, `Get-Disk`, `Get-Partition` — prefer CLI

---

## Quick Settings Panel (Win+A)
**Launch:** Win+A hotkey

| Element | X | Y | Notes |
|---------|---|---|-------|
| WiFi toggle | 1700 | 900 | Bottom-right cluster |
| Bluetooth toggle | 1770 | 900 | |
| Airplane mode | 1840 | 900 | |
| Night light | 1700 | 830 | |
| Brightness slider | 1770 | 750 | |
| Volume slider | 1770 | 700 | |

---

## Common Patterns

### Confirmation Dialogs (generic)
Most Windows confirmation dialogs center on screen:
- **OK/Yes (left):** ~870, 540-660
- **Cancel/No (right):** ~1050, 540-660

### File Dialogs (Save As / Open)
- **Filename field:** 700, 580
- **Save/Open button:** 1100, 630
- **Cancel button:** 1200, 630
- **File type dropdown:** 1100, 580

### Right-Click Context Menus
Appear at cursor position, items spaced ~25px vertically:
- First item: cursor_y + 25
- Second item: cursor_y + 50
- etc.

---

## Helper Functions

```powershell
# Click at coordinates
function Click-At($x, $y) {
    Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class Clicker {
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int X, int Y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint f, int dx, int dy, uint d, UIntPtr e);
    public static void Click(int x, int y) {
        SetCursorPos(x, y);
        System.Threading.Thread.Sleep(100);
        mouse_event(0x0002, 0, 0, 0, UIntPtr.Zero);
        mouse_event(0x0004, 0, 0, 0, UIntPtr.Zero);
    }
}
"@
    [Clicker]::Click($x, $y)
}

# Type text
function Type-Text($text) {
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait($text)
}

# Press key combo
function Press-Keys($keys) {
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.SendKeys]::SendWait($keys)
}
# Examples: Press-Keys "^s" (Ctrl+S), Press-Keys "%{F4}" (Alt+F4), Press-Keys "{ENTER}"
```

---

## Limitations

1. **Secure Desktop (UAC):** Standard input injection blocked. SendInput sometimes works.
2. **Resolution dependence:** Coordinates assume 1920x1080. Scale proportionally.
3. **DPI scaling:** 125%/150% scaling shifts coordinates. Divide by scale factor.
4. **Window position:** Assumes maximized/default positions. Use window management first.
5. **Animation delays:** Add `Start-Sleep -Milliseconds 300` between actions.

---

*Updated: 2026-02-13*
