#!/usr/bin/env python3
"""
Claude Code Desktop AutoUI Controller
Run from Windows Python (not WSL) for GUI access.

Usage:
    python claude-desktop-autoui.py status      # Check if Claude window exists
    python claude-desktop-autoui.py focus       # Bring Claude to foreground
    python claude-desktop-autoui.py screenshot  # Save screenshot of Claude window
    python claude-desktop-autoui.py prompt "Your message here"  # Send a prompt
    python claude-desktop-autoui.py recover     # Recovery sequence if stuck
"""

import sys
import time
import os
import ctypes
from ctypes import wintypes
from datetime import datetime

try:
    import pyautogui
    from PIL import ImageGrab
except ImportError:
    print("ERROR: pyautogui/pillow not installed. Run: pip install pyautogui pillow")
    sys.exit(1)

# Safety settings
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
pyautogui.PAUSE = 0.1  # Small delay between actions

SCREENSHOT_DIR = r"C:\Users\user\.openclaw\workspace\screenshots"

# Win32 API setup
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def get_window_process_name(hwnd):
    """Get the process name for a window handle."""
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    
    PROCESS_QUERY_INFORMATION = 0x0400
    PROCESS_VM_READ = 0x0010
    
    handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid.value)
    if not handle:
        return None
    
    try:
        name_buffer = ctypes.create_unicode_buffer(260)
        size = wintypes.DWORD(260)
        if kernel32.QueryFullProcessImageNameW(handle, 0, name_buffer, ctypes.byref(size)):
            path = name_buffer.value
            return path.split('\\')[-1].lower()
    finally:
        kernel32.CloseHandle(handle)
    return None

def get_window_rect(hwnd):
    """Get window rectangle."""
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return (rect.left, rect.top, rect.right, rect.bottom)

def find_claude_code_hwnd():
    """Find Claude Code window handle (claude.exe, not telegram.exe)."""
    result = [None]
    
    def callback(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
            
        title_buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title_buffer, length + 1)
        title = title_buffer.value
        
        if 'Claude' in title:
            proc_name = get_window_process_name(hwnd)
            if proc_name == 'claude.exe':
                result[0] = {'hwnd': hwnd, 'title': title}
                return False  # Stop enumeration
        return True
    
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(callback), 0)
    
    return result[0]

def status():
    """Check Claude window status."""
    info = find_claude_code_hwnd()
    if info:
        hwnd = info['hwnd']
        rect = get_window_rect(hwnd)
        is_minimized = user32.IsIconic(hwnd)
        is_foreground = user32.GetForegroundWindow() == hwnd
        
        print(f"FOUND: '{info['title']}' (claude.exe)")
        print(f"  Handle: {hwnd}")
        print(f"  Position: ({rect[0]}, {rect[1]})")
        print(f"  Size: {rect[2]-rect[0]}x{rect[3]-rect[1]}")
        print(f"  Minimized: {bool(is_minimized)}")
        print(f"  Foreground: {is_foreground}")
        return True
    else:
        print("NOT FOUND: Claude Code desktop not running")
        return False

def focus():
    """Bring Claude window to foreground."""
    info = find_claude_code_hwnd()
    if not info:
        print("ERROR: Claude Code not found")
        return False
    
    hwnd = info['hwnd']
    
    # Restore if minimized
    SW_RESTORE = 9
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, SW_RESTORE)
        time.sleep(0.3)
    
    # Bring to foreground
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.2)
    
    print(f"FOCUSED: '{info['title']}'")
    return True

def screenshot(filename=None):
    """Take screenshot of Claude window."""
    info = find_claude_code_hwnd()
    if not info:
        print("ERROR: Claude Code not found")
        return None
    
    # Ensure screenshot dir exists
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SCREENSHOT_DIR, f"claude_{timestamp}.png")
    
    hwnd = info['hwnd']
    rect = get_window_rect(hwnd)
    
    # Capture the window region
    img = ImageGrab.grab(bbox=rect)
    img.save(filename)
    print(f"SAVED: {filename}")
    return filename

def send_prompt(text):
    """Send a text prompt to Claude Code."""
    info = find_claude_code_hwnd()
    if not info:
        print("ERROR: Claude Code not found")
        return False
    
    if not focus():
        return False
    
    time.sleep(0.5)
    
    hwnd = info['hwnd']
    rect = get_window_rect(hwnd)
    
    # Click in the input area (bottom center of window)
    input_x = (rect[0] + rect[2]) // 2
    input_y = rect[3] - 100  # Near bottom
    
    pyautogui.click(input_x, input_y)
    time.sleep(0.3)
    
    # For ASCII text, type directly; for Unicode, use clipboard
    if text.isascii():
        pyautogui.typewrite(text, interval=0.02)
    else:
        import subprocess
        # Use clip.exe for clipboard
        p = subprocess.Popen(['clip'], stdin=subprocess.PIPE)
        p.communicate(input=text.encode('utf-16-le'))
        pyautogui.hotkey('ctrl', 'v')
    
    time.sleep(0.1)
    
    # Press Enter to submit
    pyautogui.press('enter')
    print(f"SENT: {text[:50]}{'...' if len(text) > 50 else ''}")
    return True

def recover():
    """Recovery sequence for stuck Claude Code."""
    print("Starting recovery sequence...")
    
    info = find_claude_code_hwnd()
    if not info:
        print("ERROR: Claude Code not found - manual restart needed")
        return False
    
    # 1. Focus the window
    focus()
    time.sleep(0.5)
    
    # 2. Try Escape to cancel any dialogs
    pyautogui.press('escape')
    time.sleep(0.3)
    
    # 3. Ctrl+C to interrupt any running command
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.5)
    
    # 4. Take diagnostic screenshot
    screenshot()
    
    print("RECOVERY: Sequence complete. Check screenshot for status.")
    return True

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == 'status':
        status()
    elif cmd == 'focus':
        focus()
    elif cmd == 'screenshot':
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        screenshot(filename)
    elif cmd == 'prompt':
        if len(sys.argv) < 3:
            print("ERROR: prompt requires text argument")
            return
        send_prompt(' '.join(sys.argv[2:]))
    elif cmd == 'recover':
        recover()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == '__main__':
    main()
