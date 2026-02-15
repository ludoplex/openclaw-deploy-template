# Smart Click - ML-style probabilistic targeting
# Implements Hunt-Target algorithm like optimal Battleship AI

param(
    [string]$WindowTitle = "Claude",
    [string]$TargetArea = "center",  # center, input, button
    [int]$Clicks = 5,
    [int]$SpreadPx = 20,
    [switch]$DryRun
)

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class WinAPI {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
    
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);
    
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;
    
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT {
        public int Left;
        public int Top;
        public int Right;
        public int Bottom;
    }
    
    public static void Click(int x, int y) {
        SetCursorPos(x, y);
        System.Threading.Thread.Sleep(50);
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    }
}
"@

# Find target window
$proc = Get-Process | Where-Object { $_.MainWindowTitle -like "*$WindowTitle*" -and $_.MainWindowHandle -ne 0 } | Select-Object -First 1

if (-not $proc) {
    Write-Host "Window '$WindowTitle' not found" -ForegroundColor Red
    exit 1
}

Write-Host "Found window: $($proc.MainWindowTitle) (PID: $($proc.Id))" -ForegroundColor Green

# Get window bounds
$rect = New-Object WinAPI+RECT
[WinAPI]::GetWindowRect($proc.MainWindowHandle, [ref]$rect) | Out-Null

$winWidth = $rect.Right - $rect.Left
$winHeight = $rect.Bottom - $rect.Top

Write-Host "Window bounds: ($($rect.Left), $($rect.Top)) to ($($rect.Right), $($rect.Bottom))"
Write-Host "Size: ${winWidth}x${winHeight}"

# Calculate target center based on area
switch ($TargetArea) {
    "center" {
        $centerX = $rect.Left + ($winWidth / 2)
        $centerY = $rect.Top + ($winHeight / 2)
    }
    "input" {
        # Bottom center - typical input area
        $centerX = $rect.Left + ($winWidth / 2)
        $centerY = $rect.Bottom - 100
    }
    "button" {
        # Bottom right - typical button area
        $centerX = $rect.Right - 100
        $centerY = $rect.Bottom - 50
    }
    default {
        $centerX = $rect.Left + ($winWidth / 2)
        $centerY = $rect.Top + ($winHeight / 2)
    }
}

Write-Host "Target area: $TargetArea -> ($centerX, $centerY)" -ForegroundColor Cyan

# Focus window first
[WinAPI]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
Start-Sleep -Milliseconds 300

# ML-style probability distribution (Gaussian-like spread from center)
# Each click slightly offset, converging on most likely target
$offsets = @(
    @(0, 0),        # Center - highest probability
    @(-0.5, -0.3),  # Slight offsets
    @(0.5, 0.3),
    @(-0.3, 0.5),
    @(0.3, -0.5),
    @(-0.8, 0),     # Further exploration
    @(0.8, 0),
    @(0, -0.8),
    @(0, 0.8)
)

Write-Host "`n=== Executing Clicks ===" -ForegroundColor Yellow

for ($i = 0; $i -lt $Clicks -and $i -lt $offsets.Count; $i++) {
    $ox = $offsets[$i][0] * $SpreadPx
    $oy = $offsets[$i][1] * $SpreadPx
    
    $clickX = [int]($centerX + $ox)
    $clickY = [int]($centerY + $oy)
    
    Write-Host "Click $($i+1): ($clickX, $clickY)" -NoNewline
    
    if (-not $DryRun) {
        [WinAPI]::Click($clickX, $clickY)
        Write-Host " [CLICKED]" -ForegroundColor Green
        Start-Sleep -Milliseconds 150
    } else {
        Write-Host " [DRY RUN]" -ForegroundColor Gray
    }
}

Write-Host "`nDone!" -ForegroundColor Green
