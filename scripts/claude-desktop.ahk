; Claude Code Desktop Controller - AutoHotkey v2
; Hotkeys:
;   Win+C     = Focus Claude Code
;   Win+Alt+C = Recovery sequence (Escape + Ctrl+C)
;   Win+Shift+C = Screenshot Claude window
;
; Runs in system tray. Right-click tray icon for menu.

#Requires AutoHotkey v2.0
#SingleInstance Force
Persistent

; Tray setup
TraySetIcon("shell32.dll", 278)  ; Purple/blue icon
A_IconTip := "Claude Code Controller"

; Create tray menu
tray := A_TrayMenu
tray.Delete()  ; Clear default
tray.Add("Focus Claude (Win+C)", (*) => FocusClaude())
tray.Add("Recovery (Win+Alt+C)", (*) => RecoverClaude())
tray.Add("Screenshot (Win+Shift+C)", (*) => ScreenshotClaude())
tray.Add()
tray.Add("Exit", (*) => ExitApp())

; ========== HOTKEYS ==========

; Win+C = Focus Claude Code
#c:: FocusClaude()

; Win+Alt+C = Recovery sequence  
#!c:: RecoverClaude()

; Win+Shift+C = Screenshot
#+c:: ScreenshotClaude()

; ========== FUNCTIONS ==========

FindClaudeWindow() {
    ; Find window with title "Claude" belonging to claude.exe
    windows := WinGetList("Claude")
    for hwnd in windows {
        try {
            pid := WinGetPID(hwnd)
            procName := ProcessGetName(pid)
            if (procName = "claude.exe") {
                return hwnd
            }
        }
    }
    return 0
}

FocusClaude() {
    hwnd := FindClaudeWindow()
    if (!hwnd) {
        TrayTip("Claude Code not found", "Is it running?", "Icon!")
        return false
    }
    
    ; Restore if minimized
    if WinGetMinMax(hwnd) = -1
        WinRestore(hwnd)
    
    ; Activate (bring to front)
    WinActivate(hwnd)
    WinMoveTop(hwnd)
    
    TrayTip("Claude Code", "Window focused", "Icon1")
    return true
}

RecoverClaude() {
    if (!FocusClaude())
        return
    
    Sleep(300)
    
    ; Press Escape to dismiss dialogs
    Send("{Escape}")
    Sleep(200)
    
    ; Ctrl+C to interrupt running commands
    Send("^c")
    Sleep(200)
    
    TrayTip("Claude Code", "Recovery sequence sent", "Icon1")
}

ScreenshotClaude() {
    hwnd := FindClaudeWindow()
    if (!hwnd) {
        TrayTip("Claude Code not found", "Is it running?", "Icon!")
        return
    }
    
    ; Get window position
    WinGetPos(&x, &y, &w, &h, hwnd)
    
    ; Create screenshot directory
    screenshotDir := A_MyDocuments . "\..\\.openclaw\workspace\screenshots"
    if !DirExist(screenshotDir)
        DirCreate(screenshotDir)
    
    ; Generate filename with timestamp
    timestamp := FormatTime(, "yyyyMMdd_HHmmss")
    filename := screenshotDir . "\claude_ahk_" . timestamp . ".png"
    
    ; Use built-in screenshot (captures to clipboard, then save)
    ; For now, just copy region to clipboard
    FocusClaude()
    Sleep(200)
    Send("{PrintScreen}")
    
    TrayTip("Screenshot", "Copied to clipboard`nSave manually for now", "Icon1")
}

; Startup notification
TrayTip("Claude Controller", "Running in background`nWin+C to focus Claude", "Icon1")
