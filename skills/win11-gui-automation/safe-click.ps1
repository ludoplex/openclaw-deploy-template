# Safe Click - Avoids Cancel/Close danger zones
# Implements "safe harbor" targeting for GUI automation

param(
    [string]$WindowTitle = "Claude",
    [int]$Clicks = 3,
    [int]$SpreadPx = 10,
    [switch]$DryRun
)

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class SafeClick {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
    
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);
    
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;
    
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT {
        public int Left, Top, Right, Bottom;
    }
    
    public static void Click(int x, int y) {
        SetCursorPos(x, y);
        System.Threading.Thread.Sleep(50);
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    }
}
"@

# Find window
$proc = Get-Process | Where-Object { $_.MainWindowTitle -like "*$WindowTitle*" -and $_.MainWindowHandle -ne 0 } | Select-Object -First 1

if (-not $proc) {
    Write-Host "Window '$WindowTitle' not found" -ForegroundColor Red
    exit 1
}

$rect = New-Object SafeClick+RECT
[SafeClick]::GetWindowRect($proc.MainWindowHandle, [ref]$rect) | Out-Null

$w = $rect.Right - $rect.Left
$h = $rect.Bottom - $rect.Top

Write-Host "Window: $($proc.MainWindowTitle)" -ForegroundColor Green
Write-Host "Size: ${w}x${h}"

# === DANGER ZONES (Cancel/Close buttons typically here) ===
# Avoid: Bottom-right quadrant, top-right corner (X button), any edge
$dangerZones = @(
    @{name="Bottom-Right"; x1=0.65; y1=0.85; x2=1.0; y2=1.0},   # Cancel buttons
    @{name="Top-Right"; x1=0.90; y1=0.0; x2=1.0; y2=0.08},      # Window X button
    @{name="Right-Edge"; x1=0.92; y1=0.0; x2=1.0; y2=1.0},      # Right edge
    @{name="Bottom-Edge"; x1=0.0; y1=0.95; x2=1.0; y2=1.0},     # Very bottom
    @{name="Top-Edge"; x1=0.0; y1=0.0; x2=1.0; y2=0.05}         # Title bar
)

# === SAFE ZONE: Left-center to center-bottom (input areas, content) ===
# Target: Center-left of bottom half (where text input usually is)
$safeX = $rect.Left + ($w * 0.35)  # 35% from left
$safeY = $rect.Top + ($h * 0.80)   # 80% down (but not at very bottom)

function Test-InDangerZone {
    param($x, $y)
    
    $relX = ($x - $rect.Left) / $w
    $relY = ($y - $rect.Top) / $h
    
    foreach ($zone in $dangerZones) {
        if ($relX -ge $zone.x1 -and $relX -le $zone.x2 -and
            $relY -ge $zone.y1 -and $relY -le $zone.y2) {
            return $zone.name
        }
    }
    return $null
}

Write-Host "`nSafe target zone: ($([int]$safeX), $([int]$safeY))" -ForegroundColor Cyan
Write-Host "Avoiding: Bottom-right, Top-right (X), Edges" -ForegroundColor Yellow

[SafeClick]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 300

# Click pattern biased LEFT of center (away from Cancel)
$offsets = @(
    @(0, 0),
    @(-0.8, -0.2),   # Go LEFT
    @(-0.5, 0.3),    # Stay left
    @(-1.0, 0),      # Further left
    @(-0.3, -0.5)    # Upper left
)

Write-Host "`n=== Safe Clicks ===" -ForegroundColor Green

for ($i = 0; $i -lt $Clicks -and $i -lt $offsets.Count; $i++) {
    $clickX = [int]($safeX + ($offsets[$i][0] * $SpreadPx))
    $clickY = [int]($safeY + ($offsets[$i][1] * $SpreadPx))
    
    # Safety check
    $danger = Test-InDangerZone $clickX $clickY
    if ($danger) {
        Write-Host "Click $($i+1): ($clickX, $clickY) - BLOCKED (in $danger zone)" -ForegroundColor Red
        continue
    }
    
    Write-Host "Click $($i+1): ($clickX, $clickY)" -NoNewline
    
    if (-not $DryRun) {
        [SafeClick]::Click($clickX, $clickY)
        Write-Host " [SAFE CLICK]" -ForegroundColor Green
        Start-Sleep -Milliseconds 150
    } else {
        Write-Host " [DRY RUN]" -ForegroundColor Gray
    }
}

Write-Host "`nCompleted safely!" -ForegroundColor Green
