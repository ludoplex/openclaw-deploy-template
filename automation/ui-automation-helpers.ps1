# Windows UI Automation Helpers
# Source this file: . .\ui-automation-helpers.ps1

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

# Core click function using SendInput (more reliable than mouse_event)
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Threading;

public class UIAuto {
    [DllImport("user32.dll", SetLastError = true)]
    public static extern uint SendInput(uint nInputs, INPUT[] pInputs, int cbSize);
    
    [DllImport("user32.dll")]
    public static extern bool SetCursorPos(int X, int Y);
    
    [DllImport("user32.dll")]
    public static extern bool GetCursorPos(out POINT lpPoint);
    
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    
    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);
    
    [StructLayout(LayoutKind.Sequential)]
    public struct POINT { public int X; public int Y; }
    
    [StructLayout(LayoutKind.Sequential)]
    public struct INPUT {
        public uint type;
        public InputUnion U;
    }
    
    [StructLayout(LayoutKind.Explicit)]
    public struct InputUnion {
        [FieldOffset(0)] public MOUSEINPUT mi;
        [FieldOffset(0)] public KEYBDINPUT ki;
    }
    
    [StructLayout(LayoutKind.Sequential)]
    public struct MOUSEINPUT {
        public int dx, dy;
        public uint mouseData, dwFlags, time;
        public IntPtr dwExtraInfo;
    }
    
    [StructLayout(LayoutKind.Sequential)]
    public struct KEYBDINPUT {
        public ushort wVk, wScan;
        public uint dwFlags, time;
        public IntPtr dwExtraInfo;
    }
    
    public const uint INPUT_MOUSE = 0, INPUT_KEYBOARD = 1;
    public const uint MOUSEEVENTF_LEFTDOWN = 0x0002, MOUSEEVENTF_LEFTUP = 0x0004;
    public const uint MOUSEEVENTF_RIGHTDOWN = 0x0008, MOUSEEVENTF_RIGHTUP = 0x0010;
    public const uint KEYEVENTF_KEYUP = 0x0002;
    
    public static void Click(int x, int y) {
        SetCursorPos(x, y);
        Thread.Sleep(50);
        INPUT[] inputs = new INPUT[2];
        inputs[0].type = INPUT_MOUSE;
        inputs[0].U.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
        inputs[1].type = INPUT_MOUSE;
        inputs[1].U.mi.dwFlags = MOUSEEVENTF_LEFTUP;
        SendInput(2, inputs, Marshal.SizeOf(typeof(INPUT)));
    }
    
    public static void RightClick(int x, int y) {
        SetCursorPos(x, y);
        Thread.Sleep(50);
        INPUT[] inputs = new INPUT[2];
        inputs[0].type = INPUT_MOUSE;
        inputs[0].U.mi.dwFlags = MOUSEEVENTF_RIGHTDOWN;
        inputs[1].type = INPUT_MOUSE;
        inputs[1].U.mi.dwFlags = MOUSEEVENTF_RIGHTUP;
        SendInput(2, inputs, Marshal.SizeOf(typeof(INPUT)));
    }
    
    public static void DoubleClick(int x, int y) {
        Click(x, y);
        Thread.Sleep(50);
        Click(x, y);
    }
    
    public static void PressKey(ushort vk) {
        INPUT[] inputs = new INPUT[2];
        inputs[0].type = INPUT_KEYBOARD;
        inputs[0].U.ki.wVk = vk;
        inputs[1].type = INPUT_KEYBOARD;
        inputs[1].U.ki.wVk = vk;
        inputs[1].U.ki.dwFlags = KEYEVENTF_KEYUP;
        SendInput(2, inputs, Marshal.SizeOf(typeof(INPUT)));
    }
    
    public static string GetActiveWindowTitle() {
        IntPtr hwnd = GetForegroundWindow();
        System.Text.StringBuilder sb = new System.Text.StringBuilder(256);
        GetWindowText(hwnd, sb, 256);
        return sb.ToString();
    }
}
"@ -ErrorAction SilentlyContinue

# Friendly wrapper functions
function Click-At {
    param([int]$X, [int]$Y, [int]$DelayMs = 100)
    [UIAuto]::Click($X, $Y)
    Start-Sleep -Milliseconds $DelayMs
}

function RightClick-At {
    param([int]$X, [int]$Y, [int]$DelayMs = 100)
    [UIAuto]::RightClick($X, $Y)
    Start-Sleep -Milliseconds $DelayMs
}

function DoubleClick-At {
    param([int]$X, [int]$Y, [int]$DelayMs = 100)
    [UIAuto]::DoubleClick($X, $Y)
    Start-Sleep -Milliseconds $DelayMs
}

function Type-Text {
    param([string]$Text, [int]$DelayMs = 50)
    [System.Windows.Forms.SendKeys]::SendWait($Text)
    Start-Sleep -Milliseconds $DelayMs
}

function Press-Keys {
    param([string]$Keys)
    # SendKeys format: ^=Ctrl, %=Alt, +=Shift, {KEY}=special keys
    # Examples: "^s" (Ctrl+S), "%{F4}" (Alt+F4), "{ENTER}", "^%{DELETE}"
    [System.Windows.Forms.SendKeys]::SendWait($Keys)
}

function Get-ActiveWindow {
    [UIAuto]::GetActiveWindowTitle()
}

function Wait-ForWindow {
    param([string]$TitlePattern, [int]$TimeoutSec = 30)
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    while ($sw.Elapsed.TotalSeconds -lt $TimeoutSec) {
        $title = Get-ActiveWindow
        if ($title -match $TitlePattern) {
            return $true
        }
        Start-Sleep -Milliseconds 200
    }
    return $false
}

# Common UI coordinates (1920x1080)
$UI = @{
    UAC = @{
        Yes = @{ X = 870; Y = 655 }
        No = @{ X = 1050; Y = 655 }
    }
    Dialog = @{
        OK = @{ X = 870; Y = 540 }
        Cancel = @{ X = 1050; Y = 540 }
        Yes = @{ X = 800; Y = 540 }
        No = @{ X = 960; Y = 540 }
    }
    FileDialog = @{
        Filename = @{ X = 700; Y = 580 }
        Save = @{ X = 1100; Y = 630 }
        Cancel = @{ X = 1200; Y = 630 }
    }
    TaskManager = @{
        Processes = @{ X = 100; Y = 60 }
        Performance = @{ X = 200; Y = 60 }
        EndTask = @{ X = 1800; Y = 950 }
    }
}

# Approve UAC dialog
function Approve-UAC {
    param([int]$RetryCount = 3, [int]$DelayMs = 500)
    for ($i = 0; $i -lt $RetryCount; $i++) {
        $consent = Get-Process consent -ErrorAction SilentlyContinue
        if ($consent) {
            Click-At -X $UI.UAC.Yes.X -Y $UI.UAC.Yes.Y -DelayMs $DelayMs
            Start-Sleep -Milliseconds 300
            $consent = Get-Process consent -ErrorAction SilentlyContinue
            if (-not $consent) {
                Write-Host "UAC approved" -ForegroundColor Green
                return $true
            }
        } else {
            return $true  # No UAC present
        }
    }
    Write-Host "UAC approval failed" -ForegroundColor Red
    return $false
}

# Scale coordinates for different DPI
function Scale-Coords {
    param([int]$X, [int]$Y, [double]$Scale = 1.0)
    @{
        X = [int]($X / $Scale)
        Y = [int]($Y / $Scale)
    }
}

# Get current screen info
function Get-ScreenInfo {
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen
    @{
        Width = $screen.Bounds.Width
        Height = $screen.Bounds.Height
        WorkingArea = $screen.WorkingArea
    }
}

Write-Host "UI Automation Helpers loaded. Available commands:" -ForegroundColor Cyan
Write-Host "  Click-At -X <x> -Y <y>"
Write-Host "  RightClick-At -X <x> -Y <y>"
Write-Host "  DoubleClick-At -X <x> -Y <y>"
Write-Host "  Type-Text '<text>'"
Write-Host "  Press-Keys '<keys>' (^=Ctrl, %=Alt, +=Shift)"
Write-Host "  Approve-UAC"
Write-Host "  Get-ActiveWindow"
Write-Host "  Wait-ForWindow '<pattern>'"
Write-Host "  `$UI hashtable has common coordinates"
