"""Force show Claude Code window even if minimized to tray."""
import ctypes
from ctypes import wintypes
import time

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Window show commands
SW_SHOW = 5
SW_RESTORE = 9
SW_SHOWDEFAULT = 10
SW_SHOWNORMAL = 1
SW_SHOWNA = 8
SW_FORCEMINIMIZE = 11

def get_window_process_name(hwnd):
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
            return name_buffer.value.split('\\')[-1].lower()
    finally:
        kernel32.CloseHandle(handle)
    return None

def find_claude_code_hwnd():
    result = [None]
    
    def callback(hwnd, _):
        length = user32.GetWindowTextLengthW(hwnd)
        if length == 0:
            return True
            
        title_buffer = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, title_buffer, length + 1)
        title = title_buffer.value
        
        if title == 'Claude':
            proc_name = get_window_process_name(hwnd)
            if proc_name == 'claude.exe':
                result[0] = hwnd
                return False
        return True
    
    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows(WNDENUMPROC(callback), 0)
    return result[0]

def get_window_info(hwnd):
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    
    style = user32.GetWindowLongW(hwnd, -16)  # GWL_STYLE
    ex_style = user32.GetWindowLongW(hwnd, -20)  # GWL_EXSTYLE
    
    is_visible = user32.IsWindowVisible(hwnd)
    is_iconic = user32.IsIconic(hwnd)
    
    return {
        'rect': (rect.left, rect.top, rect.right, rect.bottom),
        'width': rect.right - rect.left,
        'height': rect.bottom - rect.top,
        'visible': bool(is_visible),
        'minimized': bool(is_iconic),
        'style': hex(style),
        'ex_style': hex(ex_style),
    }

def force_show(hwnd):
    """Try multiple methods to force show the window."""
    
    # First, restore if minimized
    if user32.IsIconic(hwnd):
        print("Window is minimized, restoring...")
        user32.ShowWindow(hwnd, SW_RESTORE)
        time.sleep(0.2)
    
    # Make sure it's visible
    user32.ShowWindow(hwnd, SW_SHOW)
    time.sleep(0.1)
    
    # Try to bring to foreground
    # First, use AttachThreadInput trick
    foreground_hwnd = user32.GetForegroundWindow()
    foreground_tid = user32.GetWindowThreadProcessId(foreground_hwnd, None)
    our_tid = user32.GetWindowThreadProcessId(hwnd, None)
    
    if foreground_tid != our_tid:
        user32.AttachThreadInput(foreground_tid, our_tid, True)
    
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    
    if foreground_tid != our_tid:
        user32.AttachThreadInput(foreground_tid, our_tid, False)
    
    # If window is offscreen, move it on screen
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    
    screen_width = user32.GetSystemMetrics(0)  # SM_CXSCREEN
    screen_height = user32.GetSystemMetrics(1)  # SM_CYSCREEN
    
    if rect.left < -500 or rect.top < -500 or rect.left > screen_width or rect.top > screen_height:
        print(f"Window is offscreen at ({rect.left}, {rect.top}), moving to (100, 100)")
        width = rect.right - rect.left
        height = rect.bottom - rect.top
        user32.MoveWindow(hwnd, 100, 100, width, height, True)

if __name__ == '__main__':
    hwnd = find_claude_code_hwnd()
    if not hwnd:
        print("ERROR: Claude Code window not found")
        exit(1)
    
    print(f"Found Claude Code window: hwnd={hwnd}")
    
    info = get_window_info(hwnd)
    print(f"Before:")
    for k, v in info.items():
        print(f"  {k}: {v}")
    
    print("\nForcing show...")
    force_show(hwnd)
    
    time.sleep(0.5)
    info = get_window_info(hwnd)
    print(f"\nAfter:")
    for k, v in info.items():
        print(f"  {k}: {v}")
