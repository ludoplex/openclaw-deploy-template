#!/usr/bin/env python3
"""
Windows 11 GUI Automation for OpenClaw Recovery
Uses pyautogui to interact with Claude Code Desktop if needed
"""

import subprocess
import time
import sys

try:
    import pyautogui
    import pygetwindow as gw
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyautogui", "pygetwindow"])
    import pyautogui
    import pygetwindow as gw

CLAUDE_CODE_PATH = r"C:\Users\user\AppData\Local\AnthropicClaude\app-1.1.2512\claude.exe"
RECOVERY_PROMPT_PATH = r"C:\Users\user\.openclaw\workspace\scripts\contingency\recovery-prompt.md"


def check_openclaw_health():
    """Check if OpenClaw gateway is responding"""
    try:
        import urllib.request
        response = urllib.request.urlopen("http://127.0.0.1:18790/health", timeout=5)
        return response.status == 200
    except:
        return False


def launch_claude_code():
    """Launch Claude Code Desktop if not running"""
    windows = gw.getWindowsWithTitle("Claude")
    if not windows:
        print("Launching Claude Code Desktop...")
        subprocess.Popen(CLAUDE_CODE_PATH)
        time.sleep(5)
    return gw.getWindowsWithTitle("Claude")


def focus_claude_window():
    """Bring Claude Code window to foreground"""
    windows = gw.getWindowsWithTitle("Claude")
    if windows:
        win = windows[0]
        win.activate()
        time.sleep(0.5)
        return True
    return False


def type_recovery_prompt():
    """Type the recovery prompt into Claude Code"""
    with open(RECOVERY_PROMPT_PATH, 'r') as f:
        prompt = f.read()
    
    # Focus Claude window
    if not focus_claude_window():
        launch_claude_code()
        time.sleep(3)
        if not focus_claude_window():
            print("ERROR: Could not focus Claude Code window")
            return False
    
    # Type the prompt (slowly to avoid issues)
    pyautogui.write(prompt[:500], interval=0.01)  # First 500 chars
    time.sleep(0.5)
    pyautogui.press('enter')
    
    print("Recovery prompt sent to Claude Code")
    return True


def main():
    print("=== OpenClaw Recovery via GUI Automation ===")
    
    # Check if OpenClaw is down
    if check_openclaw_health():
        print("OpenClaw gateway is healthy. No action needed.")
        return 0
    
    print("WARNING: OpenClaw gateway is DOWN!")
    print("Attempting GUI-based recovery via Claude Code...")
    
    # Try to use Claude Code for recovery
    if type_recovery_prompt():
        print("Recovery prompt sent. Monitor Claude Code for progress.")
        return 0
    else:
        print("GUI automation failed. Manual intervention required.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
