# SOURCE MANIFEST: GUI Automation on Mac M4 (Apple Silicon)

**Generated:** 2026-02-10
**Target Platform:** macOS 14+ (Sonoma) on Apple M4 (ARM64)
**Primary Framework:** PyObjC 12.x with Quartz bindings

---

## 1. INSTALLATION

### PyObjC on ARM64 Mac

```bash
# Recommended: Use native ARM64 Python (not Rosetta)
python3 -m pip install pyobjc-framework-Quartz pyobjc-framework-Cocoa

# Verify ARM64 installation
python3 -c "import objc; print(objc.arch)"  # Should print: arm64

# Specific packages
pip install pyobjc-framework-Quartz   # CoreGraphics, Quartz events
pip install pyobjc-framework-Cocoa    # AppKit, NSWorkspace
pip install pyobjc-framework-ApplicationServices  # Accessibility APIs
```

**Current Version:** pyobjc-framework-quartz 12.1 (Nov 2025)
**Wheel Support:** Native ARM64 wheels available for Python 3.10-3.14

---

## 2. QUARTZ/COREGRAPHICS EVENT SYSTEM

### 2.1 Core Imports

```python
import Quartz
from Quartz import (
    # Event Creation
    CGEventCreateMouseEvent,
    CGEventCreateKeyboardEvent,
    CGEventCreateScrollWheelEvent,
    
    # Event Posting
    CGEventPost,
    CGEventPostToPid,  # Target specific process
    
    # Event Sources
    CGEventSourceCreate,
    
    # Constants
    kCGEventNull,
    kCGEventLeftMouseDown,
    kCGEventLeftMouseUp,
    kCGEventLeftMouseDragged,
    kCGEventRightMouseDown,
    kCGEventRightMouseUp,
    kCGEventRightMouseDragged,
    kCGEventMouseMoved,
    kCGEventKeyDown,
    kCGEventKeyUp,
    kCGEventScrollWheel,
    kCGEventFlagsChanged,
    
    # Tap Locations
    kCGHIDEventTap,           # Hardware level (requires Accessibility)
    kCGSessionEventTap,       # Session level
    kCGAnnotatedSessionEventTap,
    
    # Mouse Buttons
    kCGMouseButtonLeft,       # 0
    kCGMouseButtonRight,      # 1
    kCGMouseButtonCenter,     # 2
    
    # Event Source States
    kCGEventSourceStateHIDSystemState,
    kCGEventSourceStateCombinedSessionState,
    kCGEventSourceStatePrivate,
    
    # Modifier Flags
    kCGEventFlagMaskShift,      # 0x20000 (131072)
    kCGEventFlagMaskControl,    # 0x40000 (262144)
    kCGEventFlagMaskAlternate,  # 0x80000 (524288) - Option key
    kCGEventFlagMaskCommand,    # 0x100000 (1048576)
    kCGEventFlagMaskSecondaryFn,# 0x800000 (8388608) - Fn key
)
from Quartz.CoreGraphics import CGPoint
```

---

### 2.2 CGEventSourceCreate

**C Signature:**
```c
CGEventSourceRef CGEventSourceCreate(CGEventSourceStateID stateID);
```

**Python Binding:**
```python
source = Quartz.CGEventSourceCreate(stateID: int) -> CGEventSourceRef
```

**Parameters:**
| Parameter | Type | Values |
|-----------|------|--------|
| `stateID` | `int` | `kCGEventSourceStateHIDSystemState` (1), `kCGEventSourceStateCombinedSessionState` (0), `kCGEventSourceStatePrivate` (-1) |

**Example:**
```python
# Create event source (reuse for multiple events for efficiency)
source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
```

---

### 2.3 CGEventCreateMouseEvent

**C Signature:**
```c
CGEventRef CGEventCreateMouseEvent(
    CGEventSourceRef source,
    CGEventType mouseType,
    CGPoint mouseCursorPosition,
    CGMouseButton mouseButton
);
```

**Python Binding:**
```python
event = Quartz.CGEventCreateMouseEvent(
    source: CGEventSourceRef | None,
    mouseType: int,
    mouseCursorPosition: tuple[float, float] | CGPoint,
    mouseButton: int
) -> CGEventRef
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | `CGEventSourceRef` or `None` | Event source (None uses default) |
| `mouseType` | `int` | Event type constant |
| `mouseCursorPosition` | `(x, y)` tuple or `CGPoint` | Screen coordinates (origin top-left) |
| `mouseButton` | `int` | `kCGMouseButtonLeft` (0), `kCGMouseButtonRight` (1), `kCGMouseButtonCenter` (2) |

**Mouse Event Types:**
| Constant | Value | Description |
|----------|-------|-------------|
| `kCGEventLeftMouseDown` | 1 | Left button press |
| `kCGEventLeftMouseUp` | 2 | Left button release |
| `kCGEventRightMouseDown` | 3 | Right button press |
| `kCGEventRightMouseUp` | 4 | Right button release |
| `kCGEventMouseMoved` | 5 | Mouse movement (no button) |
| `kCGEventLeftMouseDragged` | 6 | Left button drag |
| `kCGEventRightMouseDragged` | 7 | Right button drag |
| `kCGEventOtherMouseDown` | 25 | Middle/other button press |
| `kCGEventOtherMouseUp` | 26 | Middle/other button release |
| `kCGEventOtherMouseDragged` | 27 | Middle/other button drag |

**Complete Click Example:**
```python
import Quartz
import time

def click(x: float, y: float, button: int = Quartz.kCGMouseButtonLeft):
    """Perform a click at screen coordinates."""
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    point = (x, y)
    
    # Determine event types based on button
    if button == Quartz.kCGMouseButtonLeft:
        down_type = Quartz.kCGEventLeftMouseDown
        up_type = Quartz.kCGEventLeftMouseUp
    elif button == Quartz.kCGMouseButtonRight:
        down_type = Quartz.kCGEventRightMouseDown
        up_type = Quartz.kCGEventRightMouseUp
    else:
        down_type = Quartz.kCGEventOtherMouseDown
        up_type = Quartz.kCGEventOtherMouseUp
    
    # Create and post events
    down = Quartz.CGEventCreateMouseEvent(source, down_type, point, button)
    up = Quartz.CGEventCreateMouseEvent(source, up_type, point, button)
    
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
    time.sleep(0.01)  # 10ms between down/up
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)

def double_click(x: float, y: float):
    """Perform a double-click."""
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    point = (x, y)
    
    for click_count in [1, 2]:
        down = Quartz.CGEventCreateMouseEvent(
            source, Quartz.kCGEventLeftMouseDown, point, Quartz.kCGMouseButtonLeft
        )
        up = Quartz.CGEventCreateMouseEvent(
            source, Quartz.kCGEventLeftMouseUp, point, Quartz.kCGMouseButtonLeft
        )
        
        # Set click count for proper double-click detection
        Quartz.CGEventSetIntegerValueField(down, Quartz.kCGMouseEventClickState, click_count)
        Quartz.CGEventSetIntegerValueField(up, Quartz.kCGMouseEventClickState, click_count)
        
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)
        
        if click_count == 1:
            time.sleep(0.05)  # Inter-click delay

def move_mouse(x: float, y: float):
    """Move mouse cursor without clicking."""
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    event = Quartz.CGEventCreateMouseEvent(
        source, Quartz.kCGEventMouseMoved, (x, y), Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

def drag(start_x: float, start_y: float, end_x: float, end_y: float, duration: float = 0.5):
    """Perform a mouse drag operation."""
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    
    # Mouse down at start
    down = Quartz.CGEventCreateMouseEvent(
        source, Quartz.kCGEventLeftMouseDown, (start_x, start_y), Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
    
    # Interpolate drag path
    steps = int(duration * 60)  # 60 FPS
    for i in range(1, steps + 1):
        t = i / steps
        x = start_x + (end_x - start_x) * t
        y = start_y + (end_y - start_y) * t
        
        drag_event = Quartz.CGEventCreateMouseEvent(
            source, Quartz.kCGEventLeftMouseDragged, (x, y), Quartz.kCGMouseButtonLeft
        )
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, drag_event)
        time.sleep(duration / steps)
    
    # Mouse up at end
    up = Quartz.CGEventCreateMouseEvent(
        source, Quartz.kCGEventLeftMouseUp, (end_x, end_y), Quartz.kCGMouseButtonLeft
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)
```

---

### 2.4 CGEventCreateKeyboardEvent

**C Signature:**
```c
CGEventRef CGEventCreateKeyboardEvent(
    CGEventSourceRef source,
    CGKeyCode virtualKey,
    bool keyDown
);
```

**Python Binding:**
```python
event = Quartz.CGEventCreateKeyboardEvent(
    source: CGEventSourceRef | None,
    virtualKey: int,
    keyDown: bool
) -> CGEventRef
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `source` | `CGEventSourceRef` or `None` | Event source |
| `virtualKey` | `int` | macOS virtual keycode (0-127) |
| `keyDown` | `bool` | `True` for key press, `False` for release |

**Common Virtual Key Codes (macOS):**
```python
KEYCODES = {
    # Letters (QWERTY layout - physical keys, not characters)
    'a': 0, 'b': 11, 'c': 8, 'd': 2, 'e': 14, 'f': 3, 'g': 5, 'h': 4,
    'i': 34, 'j': 38, 'k': 40, 'l': 37, 'm': 46, 'n': 45, 'o': 31, 'p': 35,
    'q': 12, 'r': 15, 's': 1, 't': 17, 'u': 32, 'v': 9, 'w': 13, 'x': 7,
    'y': 16, 'z': 6,
    
    # Numbers (top row)
    '0': 29, '1': 18, '2': 19, '3': 20, '4': 21, '5': 23, '6': 22, '7': 26,
    '8': 28, '9': 25,
    
    # Special keys
    'return': 36, 'enter': 76,  # Return vs numpad Enter
    'tab': 48, 'space': 49, 'delete': 51, 'escape': 53,
    'command': 55, 'shift': 56, 'capslock': 57, 'option': 58,
    'control': 59, 'rightshift': 60, 'rightoption': 61, 'rightcontrol': 62,
    'function': 63,
    
    # Arrow keys
    'left': 123, 'right': 124, 'down': 125, 'up': 126,
    
    # Function keys
    'f1': 122, 'f2': 120, 'f3': 99, 'f4': 118, 'f5': 96, 'f6': 97,
    'f7': 98, 'f8': 100, 'f9': 101, 'f10': 109, 'f11': 103, 'f12': 111,
    'f13': 105, 'f14': 107, 'f15': 113,
    
    # Punctuation
    '-': 27, '=': 24, '[': 33, ']': 30, '\\': 42, ';': 41, "'": 39,
    '`': 50, ',': 43, '.': 47, '/': 44,
    
    # Navigation
    'home': 115, 'end': 119, 'pageup': 116, 'pagedown': 121,
    'forwarddelete': 117,
}
```

**Keyboard Event Examples:**
```python
import Quartz
import time

def press_key(keycode: int, modifiers: int = 0):
    """Press and release a single key with optional modifiers."""
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    
    # Key down
    down = Quartz.CGEventCreateKeyboardEvent(source, keycode, True)
    if modifiers:
        Quartz.CGEventSetFlags(down, modifiers)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
    
    time.sleep(0.01)
    
    # Key up
    up = Quartz.CGEventCreateKeyboardEvent(source, keycode, False)
    if modifiers:
        Quartz.CGEventSetFlags(up, modifiers)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)

def type_text(text: str, interval: float = 0.02):
    """Type a string by setting Unicode on keyboard events."""
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    
    for char in text:
        # Create a key down event (keycode 0 is placeholder)
        down = Quartz.CGEventCreateKeyboardEvent(source, 0, True)
        up = Quartz.CGEventCreateKeyboardEvent(source, 0, False)
        
        # Set the Unicode string for the character
        Quartz.CGEventKeyboardSetUnicodeString(down, len(char), char)
        Quartz.CGEventKeyboardSetUnicodeString(up, len(char), char)
        
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)
        
        time.sleep(interval)

def hotkey(*keys: int):
    """Press a key combination (e.g., Cmd+C)."""
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    
    # Press all keys
    for key in keys:
        down = Quartz.CGEventCreateKeyboardEvent(source, key, True)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, down)
        time.sleep(0.01)
    
    # Release in reverse order
    for key in reversed(keys):
        up = Quartz.CGEventCreateKeyboardEvent(source, key, False)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, up)
        time.sleep(0.01)

# Usage examples
press_key(8)  # Press 'c'
press_key(8, Quartz.kCGEventFlagMaskCommand)  # Cmd+C (copy)
type_text("Hello, World!")
hotkey(55, 8)  # Cmd+C using hotkey function
```

---

### 2.5 CGEventCreateScrollWheelEvent

**C Signature:**
```c
CGEventRef CGEventCreateScrollWheelEvent(
    CGEventSourceRef source,
    CGScrollEventUnit units,
    uint32_t wheelCount,
    int32_t wheel1,
    ...  // Additional wheels
);
```

**Python Binding:**
```python
event = Quartz.CGEventCreateScrollWheelEvent(
    source: CGEventSourceRef | None,
    units: int,
    wheelCount: int,
    wheel1: int,
    wheel2: int = 0,  # Optional horizontal
    wheel3: int = 0   # Optional (rare)
) -> CGEventRef
```

**Scroll Units:**
| Constant | Value | Description |
|----------|-------|-------------|
| `kCGScrollEventUnitPixel` | 0 | Pixel-based scrolling |
| `kCGScrollEventUnitLine` | 1 | Line-based scrolling |

**Example:**
```python
def scroll(vertical: int = 0, horizontal: int = 0, pixels: bool = True):
    """Scroll the mouse wheel.
    
    Args:
        vertical: Positive = up, Negative = down
        horizontal: Positive = right, Negative = left
        pixels: True for pixel units, False for line units
    """
    source = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    units = Quartz.kCGScrollEventUnitPixel if pixels else Quartz.kCGScrollEventUnitLine
    
    event = Quartz.CGEventCreateScrollWheelEvent(
        source, units, 2, vertical, horizontal
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

# Scroll down 100 pixels
scroll(vertical=-100)

# Scroll right 50 pixels
scroll(horizontal=50)

# Scroll up 3 lines
scroll(vertical=3, pixels=False)
```

---

### 2.6 CGEventPost

**C Signature:**
```c
void CGEventPost(CGEventTapLocation tap, CGEventRef event);
```

**Python Binding:**
```python
Quartz.CGEventPost(tap: int, event: CGEventRef) -> None
```

**Tap Locations:**
| Constant | Value | Description | Permissions |
|----------|-------|-------------|-------------|
| `kCGHIDEventTap` | 0 | Hardware level (most reliable) | Requires Accessibility |
| `kCGSessionEventTap` | 1 | Session level | Requires Accessibility |
| `kCGAnnotatedSessionEventTap` | 2 | Annotated session | Lower permission |

---

### 2.7 CGEventPostToPid (Target Specific Process)

**C Signature:**
```c
void CGEventPostToPid(pid_t pid, CGEventRef event);
```

**Python Binding:**
```python
Quartz.CGEventPostToPid(pid: int, event: CGEventRef) -> None
```

**Example:**
```python
import subprocess

def get_frontmost_app_pid() -> int:
    """Get PID of frontmost application."""
    script = 'tell application "System Events" to unix id of (first process whose frontmost is true)'
    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
    return int(result.stdout.strip())

# Post event to specific application
pid = get_frontmost_app_pid()
event = Quartz.CGEventCreateKeyboardEvent(None, 36, True)  # Return key
Quartz.CGEventPostToPid(pid, event)
```

---

### 2.8 Event Field Manipulation

```python
# Get/Set integer fields
Quartz.CGEventGetIntegerValueField(event, field) -> int
Quartz.CGEventSetIntegerValueField(event, field, value)

# Get/Set double fields  
Quartz.CGEventGetDoubleValueField(event, field) -> float
Quartz.CGEventSetDoubleValueField(event, field, value)

# Set event flags (modifiers)
Quartz.CGEventSetFlags(event, flags)
Quartz.CGEventGetFlags(event) -> int
```

**Common Event Fields:**
| Field | Constant | Description |
|-------|----------|-------------|
| `kCGMouseEventClickState` | 1 | Click count (1, 2, 3...) |
| `kCGMouseEventButtonNumber` | 3 | Button number |
| `kCGMouseEventDeltaX` | 4 | Mouse delta X |
| `kCGMouseEventDeltaY` | 5 | Mouse delta Y |
| `kCGKeyboardEventKeycode` | 9 | Virtual keycode |
| `kCGKeyboardEventAutorepeat` | 8 | Auto-repeat flag |
| `kCGScrollWheelEventDeltaAxis1` | 11 | Vertical scroll delta |
| `kCGScrollWheelEventDeltaAxis2` | 12 | Horizontal scroll delta |

---

## 3. SCREEN CAPTURE FUNCTIONS

### 3.1 CGWindowListCreateImage

**C Signature:**
```c
CGImageRef CGWindowListCreateImage(
    CGRect screenBounds,
    CGWindowListOption listOption,
    CGWindowID windowID,
    CGWindowImageOption imageOption
);
```

**Python Binding:**
```python
image = Quartz.CGWindowListCreateImage(
    screenBounds: tuple,  # (x, y, width, height) or CGRectNull for full screen
    listOption: int,
    windowID: int,
    imageOption: int
) -> CGImageRef
```

**Window List Options:**
| Constant | Value | Description |
|----------|-------|-------------|
| `kCGWindowListOptionAll` | 0 | All windows |
| `kCGWindowListOptionOnScreenOnly` | 1 | Visible windows only |
| `kCGWindowListOptionOnScreenAboveWindow` | 2 | Windows above specified |
| `kCGWindowListOptionOnScreenBelowWindow` | 4 | Windows below specified |
| `kCGWindowListOptionIncludingWindow` | 8 | Include specified window |
| `kCGWindowListExcludeDesktopElements` | 16 | Exclude desktop |

**Image Options:**
| Constant | Value | Description |
|----------|-------|-------------|
| `kCGWindowImageDefault` | 0 | Default rendering |
| `kCGWindowImageBoundsIgnoreFraming` | 1 | Ignore window frame |
| `kCGWindowImageShouldBeOpaque` | 2 | No transparency |
| `kCGWindowImageOnlyShadows` | 4 | Only window shadows |
| `kCGWindowImageBestResolution` | 8 | Best resolution (Retina) |
| `kCGWindowImageNominalResolution` | 16 | 1:1 pixel resolution |

**Example:**
```python
import Quartz
from Quartz import CGRectNull, CGRectMake
from Foundation import NSBitmapImageRep, NSPNGFileType

def capture_screen(region=None, save_path=None):
    """Capture screen or region.
    
    Args:
        region: (x, y, width, height) or None for full screen
        save_path: Path to save PNG, or None to return CGImage
    """
    if region:
        bounds = CGRectMake(*region)
    else:
        bounds = CGRectNull  # Full screen
    
    image = Quartz.CGWindowListCreateImage(
        bounds,
        Quartz.kCGWindowListOptionOnScreenOnly,
        Quartz.kCGNullWindowID,
        Quartz.kCGWindowImageDefault
    )
    
    if save_path and image:
        # Convert to NSBitmapImageRep and save as PNG
        bitmap = NSBitmapImageRep.alloc().initWithCGImage_(image)
        png_data = bitmap.representationUsingType_properties_(NSPNGFileType, None)
        png_data.writeToFile_atomically_(save_path, True)
    
    return image

def capture_window(window_id: int, save_path=None):
    """Capture a specific window by ID."""
    image = Quartz.CGWindowListCreateImage(
        CGRectNull,
        Quartz.kCGWindowListOptionIncludingWindow,
        window_id,
        Quartz.kCGWindowImageBoundsIgnoreFraming | Quartz.kCGWindowImageBestResolution
    )
    
    if save_path and image:
        bitmap = NSBitmapImageRep.alloc().initWithCGImage_(image)
        png_data = bitmap.representationUsingType_properties_(NSPNGFileType, None)
        png_data.writeToFile_atomically_(save_path, True)
    
    return image
```

---

### 3.2 CGWindowListCopyWindowInfo

```python
def get_window_list():
    """Get list of all windows with their info."""
    options = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
    window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
    
    windows = []
    for window in window_list:
        windows.append({
            'id': window.get(Quartz.kCGWindowNumber),
            'name': window.get(Quartz.kCGWindowName, ''),
            'owner': window.get(Quartz.kCGWindowOwnerName, ''),
            'pid': window.get(Quartz.kCGWindowOwnerPID),
            'bounds': window.get(Quartz.kCGWindowBounds),
            'layer': window.get(Quartz.kCGWindowLayer),
        })
    return windows

# Find window by name
def find_window(name: str):
    for w in get_window_list():
        if name.lower() in (w['name'] or '').lower():
            return w
    return None
```

---

### 3.3 CGDisplayCreateImage (Display Capture)

```python
def capture_display(display_id=None):
    """Capture entire display.
    
    Args:
        display_id: CGDirectDisplayID or None for main display
    """
    if display_id is None:
        display_id = Quartz.CGMainDisplayID()
    
    return Quartz.CGDisplayCreateImage(display_id)

def get_all_displays():
    """Get list of all display IDs."""
    max_displays = 16
    (error, display_ids, count) = Quartz.CGGetActiveDisplayList(max_displays, None, None)
    return display_ids[:count] if error == 0 else []
```

---

## 4. APPKIT / NSWORKSPACE

### 4.1 Core Imports

```python
from AppKit import (
    NSWorkspace,
    NSRunningApplication,
    NSApplicationActivateIgnoringOtherApps,
    NSApplicationActivateAllWindows,
)
from Foundation import NSURL
```

### 4.2 NSWorkspace Methods

```python
# Get shared workspace instance
workspace = NSWorkspace.sharedWorkspace()

# Launch application
workspace.launchApplication_(app_name: str) -> bool
workspace.launchApplicationAtURL_options_configuration_error_(
    url: NSURL,
    options: int,
    configuration: dict,
    error: None
) -> NSRunningApplication

# Open files
workspace.openFile_(path: str) -> bool
workspace.openFile_withApplication_(path: str, app: str) -> bool
workspace.openURL_(url: NSURL) -> bool

# Get running applications
workspace.runningApplications() -> list[NSRunningApplication]
workspace.frontmostApplication() -> NSRunningApplication

# Application info
workspace.fullPathForApplication_(app_name: str) -> str
workspace.URLForApplicationWithBundleIdentifier_(bundle_id: str) -> NSURL
```

**Complete Example:**
```python
from AppKit import NSWorkspace, NSRunningApplication, NSApplicationActivateIgnoringOtherApps
from Foundation import NSURL
import time

class AppController:
    def __init__(self):
        self.workspace = NSWorkspace.sharedWorkspace()
    
    def launch_app(self, app_name: str) -> bool:
        """Launch application by name."""
        return self.workspace.launchApplication_(app_name)
    
    def launch_app_by_bundle(self, bundle_id: str) -> NSRunningApplication:
        """Launch application by bundle identifier."""
        url = self.workspace.URLForApplicationWithBundleIdentifier_(bundle_id)
        if url:
            config = {}
            app, error = self.workspace.launchApplicationAtURL_options_configuration_error_(
                url, 0, config, None
            )
            return app
        return None
    
    def get_running_apps(self) -> list:
        """Get all running applications."""
        return [
            {
                'name': app.localizedName(),
                'bundle_id': app.bundleIdentifier(),
                'pid': app.processIdentifier(),
                'active': app.isActive(),
            }
            for app in self.workspace.runningApplications()
        ]
    
    def get_frontmost_app(self):
        """Get the frontmost application."""
        app = self.workspace.frontmostApplication()
        return {
            'name': app.localizedName(),
            'bundle_id': app.bundleIdentifier(),
            'pid': app.processIdentifier(),
        }
    
    def activate_app(self, app_name: str = None, bundle_id: str = None, pid: int = None) -> bool:
        """Bring application to front."""
        for app in self.workspace.runningApplications():
            if app_name and app.localizedName() == app_name:
                return app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            if bundle_id and app.bundleIdentifier() == bundle_id:
                return app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            if pid and app.processIdentifier() == pid:
                return app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
        return False
    
    def open_url(self, url_string: str) -> bool:
        """Open URL in default browser."""
        url = NSURL.URLWithString_(url_string)
        return self.workspace.openURL_(url)
    
    def open_file(self, path: str, app: str = None) -> bool:
        """Open file, optionally with specific app."""
        if app:
            return self.workspace.openFile_withApplication_(path, app)
        return self.workspace.openFile_(path)

# Usage
ctrl = AppController()
ctrl.launch_app("Safari")
ctrl.activate_app(bundle_id="com.apple.Safari")
ctrl.open_url("https://example.com")
```

---

### 4.3 NSRunningApplication Methods

```python
app: NSRunningApplication

# Properties
app.localizedName() -> str           # Display name
app.bundleIdentifier() -> str        # e.g., "com.apple.Safari"
app.bundleURL() -> NSURL             # Application bundle path
app.processIdentifier() -> int       # Unix PID
app.isActive() -> bool               # Is frontmost
app.isHidden() -> bool               # Is hidden
app.isFinishedLaunching() -> bool    # Launch complete

# Methods
app.activateWithOptions_(options: int) -> bool  # Bring to front
app.hide() -> bool                              # Hide application
app.unhide() -> bool                            # Unhide application
app.terminate() -> bool                         # Request quit
app.forceTerminate() -> bool                    # Force quit
```

---

## 5. ACCESSIBILITY APIs (AXUIElement)

### 5.1 Setup and Permissions

```python
from ApplicationServices import (
    AXIsProcessTrustedWithOptions,
    AXUIElementCreateApplication,
    AXUIElementCreateSystemWide,
    AXUIElementCopyAttributeValue,
    AXUIElementCopyAttributeNames,
    AXUIElementSetAttributeValue,
    AXUIElementPerformAction,
    kAXTrustedCheckOptionPrompt,
)
from Foundation import NSDictionary

def check_accessibility_permission(prompt: bool = True) -> bool:
    """Check if app has accessibility permissions."""
    options = NSDictionary.dictionaryWithObject_forKey_(
        prompt, kAXTrustedCheckOptionPrompt
    )
    return AXIsProcessTrustedWithOptions(options)
```

### 5.2 AXUIElement Operations

```python
from ApplicationServices import (
    AXUIElementCreateApplication,
    AXUIElementCopyAttributeValue,
    AXUIElementCopyAttributeNames,
    AXUIElementSetAttributeValue,
    AXUIElementPerformAction,
    AXUIElementCopyElementAtPosition,
)

def get_app_element(pid: int):
    """Get accessibility element for application."""
    return AXUIElementCreateApplication(pid)

def get_element_at_position(x: float, y: float):
    """Get UI element at screen position."""
    system = AXUIElementCreateSystemWide()
    element, error = AXUIElementCopyElementAtPosition(system, x, y, None)
    return element if error == 0 else None

def get_attribute(element, attribute: str):
    """Get attribute value from element."""
    error, value = AXUIElementCopyAttributeValue(element, attribute, None)
    return value if error == 0 else None

def set_attribute(element, attribute: str, value):
    """Set attribute value on element."""
    error = AXUIElementSetAttributeValue(element, attribute, value)
    return error == 0

def perform_action(element, action: str):
    """Perform action on element."""
    error = AXUIElementPerformAction(element, action)
    return error == 0

# Common attributes
ATTRIBUTES = {
    'role': 'AXRole',
    'title': 'AXTitle',
    'value': 'AXValue',
    'description': 'AXDescription',
    'position': 'AXPosition',
    'size': 'AXSize',
    'children': 'AXChildren',
    'parent': 'AXParent',
    'focused': 'AXFocused',
    'enabled': 'AXEnabled',
    'window': 'AXWindow',
    'windows': 'AXWindows',
    'focused_window': 'AXFocusedWindow',
}

# Common actions
ACTIONS = {
    'press': 'AXPress',
    'cancel': 'AXCancel',
    'raise': 'AXRaise',
    'show_menu': 'AXShowMenu',
    'pick': 'AXPick',
    'confirm': 'AXConfirm',
}
```

### 5.3 Complete Accessibility Example

```python
def click_button_by_title(pid: int, button_title: str) -> bool:
    """Find and click a button in an application by its title."""
    app = AXUIElementCreateApplication(pid)
    
    def find_button(element, title):
        role = get_attribute(element, 'AXRole')
        if role == 'AXButton':
            btn_title = get_attribute(element, 'AXTitle')
            if btn_title == title:
                return element
        
        children = get_attribute(element, 'AXChildren')
        if children:
            for child in children:
                result = find_button(child, title)
                if result:
                    return result
        return None
    
    button = find_button(app, button_title)
    if button:
        return perform_action(button, 'AXPress')
    return False

def get_focused_text_field():
    """Get the currently focused text field."""
    system = AXUIElementCreateSystemWide()
    focused = get_attribute(system, 'AXFocusedUIElement')
    if focused:
        role = get_attribute(focused, 'AXRole')
        if role in ('AXTextField', 'AXTextArea', 'AXComboBox'):
            return focused
    return None

def type_in_focused_field(text: str):
    """Type text into the focused field using Accessibility."""
    field = get_focused_text_field()
    if field:
        return set_attribute(field, 'AXValue', text)
    return False
```

---

## 6. PERMISSIONS REQUIRED

### 6.1 Accessibility Permission

**Required for:**
- CGEventPost to `kCGHIDEventTap` and `kCGSessionEventTap`
- CGEventTapCreate (event listening)
- AXUIElement APIs

**How to grant:**
1. System Preferences → Security & Privacy → Privacy → Accessibility
2. Add your terminal/Python app

**Programmatic check:**
```python
from ApplicationServices import AXIsProcessTrustedWithOptions
from Foundation import NSDictionary

def request_accessibility():
    options = NSDictionary.dictionaryWithObject_forKey_(
        True, "AXTrustedCheckOptionPrompt"
    )
    return AXIsProcessTrustedWithOptions(options)
```

### 6.2 Screen Recording Permission

**Required for:**
- CGWindowListCreateImage (capturing windows)
- CGDisplayCreateImage (display capture)
- Window content access

**How to grant:**
1. System Preferences → Security & Privacy → Privacy → Screen Recording
2. Add your terminal/Python app

**Note:** No programmatic check available. If capture returns blank/nil, permission is likely missing.

---

## 7. TIMING & PERFORMANCE

### 7.1 Event Posting Speed

| Operation | Typical Timing | Notes |
|-----------|---------------|-------|
| CGEventPost | ~1-5ms | Very fast |
| Key press (down+up) | 10-20ms recommended | Too fast may be missed |
| Mouse click | 10-20ms between down/up | Apps expect delay |
| Double-click | 50-100ms between clicks | System double-click threshold |
| Type character | 20-50ms per char | Varies by app |
| Scroll event | Immediate | Can be chained rapidly |

### 7.2 Recommended Delays

```python
# Minimum safe delays
KEY_PRESS_DELAY = 0.01       # Between keydown and keyup
BETWEEN_KEYS = 0.02          # Between different keypresses
CLICK_DELAY = 0.01           # Between mousedown and mouseup
DOUBLE_CLICK_GAP = 0.05      # Between clicks in double-click
DRAG_STEP_DELAY = 0.016      # 60 FPS for smooth drags
ACTION_DELAY = 0.1           # After major actions (click, etc.)
APP_SWITCH_DELAY = 0.3       # After activating different app
```

### 7.3 ARM64/M4 Considerations

- Native ARM64 Python is significantly faster than Rosetta
- Event processing is near-instant on M-series chips
- Screen capture is hardware-accelerated
- No specific M4 optimizations required in code

---

## 8. COMPLETE AUTOMATION CLASS

```python
"""
Complete GUI automation class for Mac M4
Requires: pip install pyobjc-framework-Quartz pyobjc-framework-Cocoa
"""

import time
from typing import Optional, Tuple, List, Dict, Any
import Quartz
from Quartz import (
    CGEventCreateMouseEvent, CGEventCreateKeyboardEvent,
    CGEventCreateScrollWheelEvent, CGEventPost, CGEventSetFlags,
    CGEventSetIntegerValueField, CGEventSourceCreate,
    CGWindowListCreateImage, CGWindowListCopyWindowInfo,
    kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGEventRightMouseDown,
    kCGEventRightMouseUp, kCGEventMouseMoved, kCGEventLeftMouseDragged,
    kCGEventKeyDown, kCGEventKeyUp, kCGEventScrollWheel,
    kCGMouseButtonLeft, kCGMouseButtonRight, kCGMouseButtonCenter,
    kCGHIDEventTap, kCGEventSourceStateHIDSystemState,
    kCGScrollEventUnitPixel, kCGScrollEventUnitLine,
    kCGMouseEventClickState, kCGWindowListOptionOnScreenOnly,
    kCGWindowListExcludeDesktopElements, kCGNullWindowID,
    kCGWindowImageDefault, kCGEventFlagMaskCommand, kCGEventFlagMaskShift,
    kCGEventFlagMaskControl, kCGEventFlagMaskAlternate,
    CGRectNull, CGRectMake,
)
from AppKit import NSWorkspace, NSApplicationActivateIgnoringOtherApps
from Foundation import NSURL, NSBitmapImageRep


class MacAutomation:
    """High-level Mac GUI automation using native Quartz APIs."""
    
    # Virtual keycodes
    KEYS = {
        'a': 0, 'b': 11, 'c': 8, 'd': 2, 'e': 14, 'f': 3, 'g': 5, 'h': 4,
        'i': 34, 'j': 38, 'k': 40, 'l': 37, 'm': 46, 'n': 45, 'o': 31, 'p': 35,
        'q': 12, 'r': 15, 's': 1, 't': 17, 'u': 32, 'v': 9, 'w': 13, 'x': 7,
        'y': 16, 'z': 6,
        '0': 29, '1': 18, '2': 19, '3': 20, '4': 21, '5': 23, '6': 22, '7': 26,
        '8': 28, '9': 25,
        'return': 36, 'enter': 76, 'tab': 48, 'space': 49, 'delete': 51,
        'escape': 53, 'command': 55, 'shift': 56, 'option': 58, 'control': 59,
        'left': 123, 'right': 124, 'down': 125, 'up': 126,
        'f1': 122, 'f2': 120, 'f3': 99, 'f4': 118, 'f5': 96, 'f6': 97,
        'f7': 98, 'f8': 100, 'f9': 101, 'f10': 109, 'f11': 103, 'f12': 111,
    }
    
    MODIFIERS = {
        'command': kCGEventFlagMaskCommand,
        'cmd': kCGEventFlagMaskCommand,
        'shift': kCGEventFlagMaskShift,
        'control': kCGEventFlagMaskControl,
        'ctrl': kCGEventFlagMaskControl,
        'option': kCGEventFlagMaskAlternate,
        'alt': kCGEventFlagMaskAlternate,
    }
    
    def __init__(self):
        self.source = CGEventSourceCreate(kCGEventSourceStateHIDSystemState)
        self.workspace = NSWorkspace.sharedWorkspace()
        self.default_delay = 0.01
    
    # === MOUSE ===
    
    def move(self, x: float, y: float):
        """Move mouse to position."""
        event = CGEventCreateMouseEvent(
            self.source, kCGEventMouseMoved, (x, y), kCGMouseButtonLeft
        )
        CGEventPost(kCGHIDEventTap, event)
    
    def click(self, x: float, y: float, button: str = 'left', count: int = 1):
        """Click at position. button: 'left', 'right', 'middle'"""
        button_map = {'left': kCGMouseButtonLeft, 'right': kCGMouseButtonRight, 'middle': kCGMouseButtonCenter}
        btn = button_map.get(button, kCGMouseButtonLeft)
        
        down_type = {kCGMouseButtonLeft: kCGEventLeftMouseDown, kCGMouseButtonRight: kCGEventRightMouseDown}.get(btn, 25)
        up_type = {kCGMouseButtonLeft: kCGEventLeftMouseUp, kCGMouseButtonRight: kCGEventRightMouseUp}.get(btn, 26)
        
        for click_num in range(1, count + 1):
            down = CGEventCreateMouseEvent(self.source, down_type, (x, y), btn)
            up = CGEventCreateMouseEvent(self.source, up_type, (x, y), btn)
            CGEventSetIntegerValueField(down, kCGMouseEventClickState, click_num)
            CGEventSetIntegerValueField(up, kCGMouseEventClickState, click_num)
            CGEventPost(kCGHIDEventTap, down)
            time.sleep(self.default_delay)
            CGEventPost(kCGHIDEventTap, up)
            if click_num < count:
                time.sleep(0.05)
    
    def double_click(self, x: float, y: float):
        """Double-click at position."""
        self.click(x, y, count=2)
    
    def right_click(self, x: float, y: float):
        """Right-click at position."""
        self.click(x, y, button='right')
    
    def drag(self, start: Tuple[float, float], end: Tuple[float, float], duration: float = 0.5):
        """Drag from start to end position."""
        down = CGEventCreateMouseEvent(self.source, kCGEventLeftMouseDown, start, kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, down)
        
        steps = max(int(duration * 60), 10)
        for i in range(1, steps + 1):
            t = i / steps
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            drag = CGEventCreateMouseEvent(self.source, kCGEventLeftMouseDragged, (x, y), kCGMouseButtonLeft)
            CGEventPost(kCGHIDEventTap, drag)
            time.sleep(duration / steps)
        
        up = CGEventCreateMouseEvent(self.source, kCGEventLeftMouseUp, end, kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, up)
    
    def scroll(self, vertical: int = 0, horizontal: int = 0, pixels: bool = True):
        """Scroll. Positive = up/right, Negative = down/left."""
        units = kCGScrollEventUnitPixel if pixels else kCGScrollEventUnitLine
        event = CGEventCreateScrollWheelEvent(self.source, units, 2, vertical, horizontal)
        CGEventPost(kCGHIDEventTap, event)
    
    # === KEYBOARD ===
    
    def press(self, key: str, modifiers: List[str] = None):
        """Press a key with optional modifiers."""
        keycode = self.KEYS.get(key.lower())
        if keycode is None:
            raise ValueError(f"Unknown key: {key}")
        
        flags = 0
        if modifiers:
            for mod in modifiers:
                flags |= self.MODIFIERS.get(mod.lower(), 0)
        
        down = CGEventCreateKeyboardEvent(self.source, keycode, True)
        up = CGEventCreateKeyboardEvent(self.source, keycode, False)
        if flags:
            CGEventSetFlags(down, flags)
            CGEventSetFlags(up, flags)
        
        CGEventPost(kCGHIDEventTap, down)
        time.sleep(self.default_delay)
        CGEventPost(kCGHIDEventTap, up)
    
    def hotkey(self, *keys: str):
        """Press key combination. e.g., hotkey('command', 'c')"""
        keycodes = [self.KEYS.get(k.lower()) for k in keys]
        if None in keycodes:
            raise ValueError(f"Unknown key in: {keys}")
        
        for kc in keycodes:
            down = CGEventCreateKeyboardEvent(self.source, kc, True)
            CGEventPost(kCGHIDEventTap, down)
            time.sleep(0.01)
        
        for kc in reversed(keycodes):
            up = CGEventCreateKeyboardEvent(self.source, kc, False)
            CGEventPost(kCGHIDEventTap, up)
            time.sleep(0.01)
    
    def type_text(self, text: str, interval: float = 0.02):
        """Type a string of text."""
        for char in text:
            down = CGEventCreateKeyboardEvent(self.source, 0, True)
            up = CGEventCreateKeyboardEvent(self.source, 0, False)
            Quartz.CGEventKeyboardSetUnicodeString(down, len(char), char)
            Quartz.CGEventKeyboardSetUnicodeString(up, len(char), char)
            CGEventPost(kCGHIDEventTap, down)
            CGEventPost(kCGHIDEventTap, up)
            time.sleep(interval)
    
    # === APPLICATION CONTROL ===
    
    def launch(self, app_name: str) -> bool:
        """Launch application by name."""
        return self.workspace.launchApplication_(app_name)
    
    def activate(self, app_name: str = None, bundle_id: str = None) -> bool:
        """Bring application to front."""
        for app in self.workspace.runningApplications():
            if app_name and app.localizedName() == app_name:
                return app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            if bundle_id and app.bundleIdentifier() == bundle_id:
                return app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
        return False
    
    def open_url(self, url: str) -> bool:
        """Open URL in default browser."""
        return self.workspace.openURL_(NSURL.URLWithString_(url))
    
    def frontmost_app(self) -> Dict[str, Any]:
        """Get info about frontmost application."""
        app = self.workspace.frontmostApplication()
        return {
            'name': app.localizedName(),
            'bundle_id': app.bundleIdentifier(),
            'pid': app.processIdentifier(),
        }
    
    # === SCREEN ===
    
    def screenshot(self, region: Tuple[float, float, float, float] = None, save_path: str = None):
        """Capture screen or region. Returns CGImage."""
        bounds = CGRectMake(*region) if region else CGRectNull
        image = CGWindowListCreateImage(
            bounds,
            kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements,
            kCGNullWindowID,
            kCGWindowImageDefault
        )
        if save_path and image:
            bitmap = NSBitmapImageRep.alloc().initWithCGImage_(image)
            png_data = bitmap.representationUsingType_properties_(4, None)  # 4 = PNG
            png_data.writeToFile_atomically_(save_path, True)
        return image
    
    def get_windows(self) -> List[Dict[str, Any]]:
        """Get list of visible windows."""
        options = kCGWindowListOptionOnScreenOnly | kCGWindowListExcludeDesktopElements
        windows = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
        return [
            {
                'id': w.get('kCGWindowNumber'),
                'name': w.get('kCGWindowName', ''),
                'owner': w.get('kCGWindowOwnerName', ''),
                'pid': w.get('kCGWindowOwnerPID'),
                'bounds': w.get('kCGWindowBounds'),
            }
            for w in windows
        ]


# Usage example
if __name__ == '__main__':
    auto = MacAutomation()
    
    # Launch Safari and navigate
    auto.launch('Safari')
    time.sleep(1)
    auto.activate(app_name='Safari')
    time.sleep(0.3)
    
    # Type URL
    auto.hotkey('command', 'l')  # Focus URL bar
    time.sleep(0.1)
    auto.type_text('https://example.com')
    auto.press('return')
    
    # Take screenshot
    time.sleep(2)
    auto.screenshot(save_path='/tmp/screenshot.png')
```

---

## 9. TROUBLESHOOTING

| Issue | Cause | Solution |
|-------|-------|----------|
| Events not working | Missing Accessibility permission | Grant in System Preferences |
| Screenshots blank | Missing Screen Recording permission | Grant in System Preferences |
| Keys typed wrong | Non-QWERTY layout | Use CGEventKeyboardSetUnicodeString |
| Double-click not detected | Click count not set | Use CGEventSetIntegerValueField |
| Events ignored by app | Using wrong tap location | Try kCGHIDEventTap |
| Slow typing | Python overhead | Use native intervals, batch events |
| M1/M4 import errors | Rosetta Python | Install native ARM64 Python |

---

## 10. REFERENCES

- [PyObjC Documentation](https://pyobjc.readthedocs.io/)
- [Apple Quartz Event Services](https://developer.apple.com/documentation/coregraphics/quartz_event_services)
- [Apple CGEvent Reference](https://developer.apple.com/documentation/coregraphics/cgevent)
- [Apple NSWorkspace](https://developer.apple.com/documentation/appkit/nsworkspace)
- [Apple Accessibility API](https://developer.apple.com/documentation/applicationservices/axuielement_h)
- [PyObjC Quartz API Notes](https://pyobjc.readthedocs.io/en/latest/apinotes/Quartz.html)
