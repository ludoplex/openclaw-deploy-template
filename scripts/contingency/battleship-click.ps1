# Battleship-style Click Pattern
# Uses probabilistic spread like ML Battleship solvers (checkerboard + hunt-target)

param(
    [int]$CenterX = 0,
    [int]$CenterY = 0,
    [int]$Spread = 50,      # Pixels between clicks
    [int]$Iterations = 9,   # Number of clicks (3x3 grid = 9)
    [int]$DelayMs = 100,    # Delay between clicks
    [switch]$DryRun         # Just show coordinates, don't click
)

Add-Type @"
using System;
using System.Runtime.InteropServices;

public class MouseOps {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
    
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);
    
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;
    
    public static void Click(int x, int y) {
        SetCursorPos(x, y);
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    }
}
"@

# If no center provided, get current mouse position
if ($CenterX -eq 0 -and $CenterY -eq 0) {
    Add-Type -AssemblyName System.Windows.Forms
    $pos = [System.Windows.Forms.Cursor]::Position
    $CenterX = $pos.X
    $CenterY = $pos.Y
    Write-Host "Using current mouse position as center: ($CenterX, $CenterY)"
}

# Battleship-style checkerboard pattern offsets
# Like a probability density function - center first, then spread out
$patterns = @(
    @{dx=0; dy=0; phase="center"},           # Hit center first
    @{dx=-1; dy=-1; phase="diagonal"},       # Checkerboard pattern
    @{dx=1; dy=1; phase="diagonal"},
    @{dx=-1; dy=1; phase="diagonal"},
    @{dx=1; dy=-1; phase="diagonal"},
    @{dx=0; dy=-1; phase="cross"},           # Cross pattern (hunt mode)
    @{dx=0; dy=1; phase="cross"},
    @{dx=-1; dy=0; phase="cross"},
    @{dx=1; dy=0; phase="cross"},
    @{dx=-2; dy=0; phase="extend"},          # Extended search
    @{dx=2; dy=0; phase="extend"},
    @{dx=0; dy=-2; phase="extend"},
    @{dx=0; dy=2; phase="extend"}
)

Write-Host "=== Battleship Click Pattern ===" -ForegroundColor Cyan
Write-Host "Center: ($CenterX, $CenterY)"
Write-Host "Spread: $Spread px"
Write-Host "Iterations: $Iterations"
Write-Host ""

$clickCount = 0
foreach ($p in $patterns) {
    if ($clickCount -ge $Iterations) { break }
    
    $targetX = $CenterX + ($p.dx * $Spread)
    $targetY = $CenterY + ($p.dy * $Spread)
    
    Write-Host "[$($clickCount + 1)] Phase: $($p.phase) -> ($targetX, $targetY)" -ForegroundColor Yellow
    
    if (-not $DryRun) {
        [MouseOps]::Click($targetX, $targetY)
        Start-Sleep -Milliseconds $DelayMs
    }
    
    $clickCount++
}

Write-Host ""
Write-Host "Completed $clickCount clicks" -ForegroundColor Green
