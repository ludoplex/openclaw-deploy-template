# Win11GuiAuto.psm1 - Windows 11 GUI Automation Module
# Uses verified coordinates from coordinates.json

$script:ModulePath = $PSScriptRoot
$script:CoordsFile = Join-Path $ModulePath "coordinates.json"
$script:Coords = $null

# Load mouse click API
Add-Type @"
using System;
using System.Runtime.InteropServices;

public class Win11Mouse {
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
    
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);
    
    [DllImport("user32.dll")]
    public static extern bool GetCursorPos(out POINT lpPoint);
    
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002;
    public const uint MOUSEEVENTF_LEFTUP = 0x0004;
    
    [StructLayout(LayoutKind.Sequential)]
    public struct POINT { public int X; public int Y; }
    
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left, Top, Right, Bottom; }
    
    public static void Click(int x, int y) {
        SetCursorPos(x, y);
        System.Threading.Thread.Sleep(50);
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0);
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0);
    }
    
    public static POINT GetPos() {
        POINT p;
        GetCursorPos(out p);
        return p;
    }
}
"@

function Load-Coordinates {
    if (-not $script:Coords) {
        $script:Coords = Get-Content $script:CoordsFile | ConvertFrom-Json
    }
    return $script:Coords
}

function Get-VerifiedClick {
    param([string]$Id)
    
    $coords = Load-Coordinates
    $click = $coords.verified_clicks | Where-Object { $_.id -eq $Id }
    if (-not $click) {
        $click = $coords.estimated_coords | Where-Object { $_.id -eq $Id }
    }
    return $click
}

function Test-InDangerZone {
    param([int]$X, [int]$Y)
    
    $coords = Load-Coordinates
    foreach ($zone in $coords.danger_zones) {
        $b = $zone.bounds
        if ($X -ge $b.x_min -and $X -le $b.x_max -and 
            $Y -ge $b.y_min -and $Y -le $b.y_max) {
            return @{
                InDanger = $true
                Zone = $zone.id
                Severity = $zone.severity
                Action = $zone.action
            }
        }
    }
    return @{ InDanger = $false }
}

function Invoke-SafeClick {
    <#
    .SYNOPSIS
    Click at coordinates after checking danger zones
    
    .PARAMETER X
    X coordinate
    
    .PARAMETER Y  
    Y coordinate
    
    .PARAMETER Id
    Use predefined click ID from coordinates.json
    
    .PARAMETER Force
    Click even if in danger zone
    #>
    param(
        [int]$X = 0,
        [int]$Y = 0,
        [string]$Id = "",
        [switch]$Force
    )
    
    # Get coords from ID if specified
    if ($Id) {
        $click = Get-VerifiedClick -Id $Id
        if ($click) {
            $X = $click.coords.x
            $Y = $click.coords.y
            Write-Host "Using $Id coordinates: ($X, $Y)" -ForegroundColor Cyan
        } else {
            Write-Error "Unknown click ID: $Id"
            return $false
        }
    }
    
    # Safety check
    $danger = Test-InDangerZone -X $X -Y $Y
    if ($danger.InDanger -and -not $Force) {
        Write-Warning "BLOCKED: ($X, $Y) is in danger zone '$($danger.Zone)'"
        Write-Warning "Action would: $($danger.Action)"
        Write-Host "Use -Force to override" -ForegroundColor Yellow
        return $false
    }
    
    # Execute click
    [Win11Mouse]::Click($X, $Y)
    Write-Host "Clicked: ($X, $Y)" -ForegroundColor Green
    return $true
}

function Invoke-ClaudeInputClick {
    <#
    .SYNOPSIS
    Click Claude Code input area (safe, verified coordinates)
    #>
    param([switch]$LeftBias)
    
    if ($LeftBias) {
        Invoke-SafeClick -Id "claude-input-safe-left"
    } else {
        Invoke-SafeClick -Id "claude-input-center"
    }
}

function Invoke-UacYesClick {
    <#
    .SYNOPSIS
    Click UAC Yes button (estimated coordinates)
    #>
    Write-Warning "Using ESTIMATED coordinates for UAC - verify manually first"
    Invoke-SafeClick -Id "uac-yes-button"
}

function Get-CurrentMousePos {
    $pos = [Win11Mouse]::GetPos()
    Write-Host "Current mouse position: ($($pos.X), $($pos.Y))"
    return $pos
}

function Record-ClickCoordinate {
    <#
    .SYNOPSIS
    Record current mouse position for future reference
    #>
    param(
        [Parameter(Mandatory)][string]$Id,
        [Parameter(Mandatory)][string]$Target,
        [Parameter(Mandatory)][string]$Element,
        [string]$Notes = ""
    )
    
    $pos = Get-CurrentMousePos
    
    $newEntry = @{
        id = $Id
        target = $Target
        element = $Element
        coords = @{ x = $pos.X; y = $pos.Y }
        status = "verified"
        verified_date = (Get-Date -Format "yyyy-MM-dd")
        notes = $Notes
    }
    
    Write-Host "`nRecorded coordinate:" -ForegroundColor Green
    $newEntry | ConvertTo-Json
    
    Write-Host "`nAdd to coordinates.json manually or use Add-VerifiedClick"
    return $newEntry
}

# Export functions
Export-ModuleMember -Function @(
    'Get-VerifiedClick',
    'Test-InDangerZone', 
    'Invoke-SafeClick',
    'Invoke-ClaudeInputClick',
    'Invoke-UacYesClick',
    'Get-CurrentMousePos',
    'Record-ClickCoordinate'
)
