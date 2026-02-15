"""Find Claude Code desktop window by process name, not just title."""
import ctypes
from ctypes import wintypes
import pyautogui

user32 = ctypes.windll.user32
psapi = ctypes.windll.psapi
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

def find_claude_code_window():
    """Find Claude Code window (claude.exe, not telegram.exe)."""
    results = []
    
    def callback(hwnd, _):
        if not user32.IsWindowVisible(hwnd):
            return True
        
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
            
        title_buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title_buffer, length + 1)
        title = title_buffer.value
        
        if 'Claude' in title or 'claude' in title.lower():
            proc_name = get_window_process_name(hwnd)
            results.append({
                'hwnd': hwnd,
                'title': title,
                'process': proc_name
            })
        return True
    
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(callback), 0)
    
    return results

if __name__ == '__main__':
    windows = find_claude_code_window()
    print("Windows with 'Claude' in title:")
    for w in windows:
        print(f"  hwnd={w['hwnd']}, process={w['process']}, title={w['title']}")
    
    # Find the actual Claude Code app
    claude_code = [w for w in windows if w['process'] == 'claude.exe']
    if claude_code:
        print(f"\nClaude Code Desktop: hwnd={claude_code[0]['hwnd']}")
    else:
        print("\nClaude Code Desktop NOT FOUND")
