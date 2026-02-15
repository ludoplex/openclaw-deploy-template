# Windows GUI Interaction via PowerShell UI Automation
# Works from WSL without X11

param(
    [string]$Action = "status",
    [string]$Text = ""
)

Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

function Get-ClaudeWindow {
    $processes = Get-Process -Name "claude" -ErrorAction SilentlyContinue
    foreach ($proc in $processes) {
        if ($proc.MainWindowHandle -ne 0) {
            return $proc
        }
    }
    return $null
}

function Focus-ClaudeWindow {
    $claude = Get-ClaudeWindow
    if ($claude) {
        $hwnd = $claude.MainWindowHandle
        Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
            [DllImport("user32.dll")]
            public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
        }
"@
        [Win32]::ShowWindow($hwnd, 9)  # SW_RESTORE
        [Win32]::SetForegroundWindow($hwnd)
        return $true
    }
    return $false
}

function Send-TextToClaude {
    param([string]$Text)
    
    if (Focus-ClaudeWindow) {
        Start-Sleep -Milliseconds 500
        
        # Use SendKeys to type
        Add-Type -AssemblyName System.Windows.Forms
        [System.Windows.Forms.SendKeys]::SendWait($Text)
        Start-Sleep -Milliseconds 200
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        
        Write-Host "Text sent to Claude Code" -ForegroundColor Green
        return $true
    } else {
        Write-Host "Could not find Claude Code window" -ForegroundColor Red
        return $false
    }
}

switch ($Action) {
    "status" {
        $claude = Get-ClaudeWindow
        if ($claude) {
            Write-Host "Claude Code is running (PID: $($claude.Id))" -ForegroundColor Green
            Write-Host "Window Title: $($claude.MainWindowTitle)"
        } else {
            Write-Host "Claude Code window not found" -ForegroundColor Yellow
        }
    }
    "focus" {
        if (Focus-ClaudeWindow) {
            Write-Host "Claude Code window focused" -ForegroundColor Green
        } else {
            Write-Host "Failed to focus Claude Code" -ForegroundColor Red
        }
    }
    "send" {
        if ($Text) {
            Send-TextToClaude -Text $Text
        } else {
            Write-Host "No text provided. Use: -Text 'your message'" -ForegroundColor Yellow
        }
    }
    "recovery" {
        $recoveryText = @"
OpenClaw (Peridot) is down. Please run:
``powershell
& "C:\Users\user\.openclaw\workspace\scripts\contingency\restart-openclaw.ps1"
``
"@
        Send-TextToClaude -Text $recoveryText
    }
    default {
        Write-Host "Actions: status, focus, send, recovery"
    }
}
