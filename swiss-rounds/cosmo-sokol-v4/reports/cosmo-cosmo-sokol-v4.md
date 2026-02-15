# cosmo-sokol Source Manifest
## Repository: ludoplex/cosmo-sokol
## Generated: 2026-02-09

---

## Architecture Overview

cosmo-sokol is a **Cosmopolitan libc** port of the [sokol](https://github.com/floooh/sokol) single-header graphics libraries. It enables building **fat portable executables** (APE format) that run natively on Linux, Windows, and macOS from a single binary.

### Key Cosmopolitan Patterns Used:
- **`cosmo_dlopen` / `cosmo_dlsym` / `cosmo_dltramp`**: Runtime dynamic library loading for platform-native libraries
- **`IsLinux()` / `IsWindows()` / `IsXnu()`**: Runtime platform detection for dispatch
- **Platform-prefixed functions**: `linux_*`, `windows_*`, `macos_*` prefixes allow compiling all backends into one binary

---

## Source Files

| File | Lines | Purpose |
|------|-------|---------|
| main.c | 107 | Demo app (cimgui + sokol) |
| win32_tweaks.c | 16 | Windows console hiding helper |
| win32_tweaks.h | 8 | Header for win32_tweaks |
| nvapi/nvapi.c | 104 | NVIDIA API integration (disable threaded optimization) |
| nvapi/nvapi.h | 10 | NVAPI header |
| nvapi/nvapi_decl.h | 155 | NVAPI type declarations |
| shims/linux/gl.c | 6172 | OpenGL function shims for Linux via cosmo_dlopen |
| shims/linux/x11.c | 507 | X11/Xcursor/Xi function shims for Linux |
| shims/sokol/sokol_cosmo.c | 3099 | Runtime dispatch layer (routes to linux_/windows_/macos_ impls) |
| shims/sokol/sokol_linux.c | 15 | Linux sokol impl setup (includes sokol with linux_ prefix) |
| shims/sokol/sokol_linux.h | 200 | Linux function prefix macros |
| shims/sokol/sokol_macos.c | 694 | macOS sokol stub implementation |
| shims/sokol/sokol_macos.h | 200 | macOS function prefix macros |
| shims/sokol/sokol_windows.c | 282 | Windows sokol impl setup (Win32 type shims) |
| shims/sokol/sokol_windows.h | 200 | Windows function prefix macros |
| shims/sokol/sokol_shared.c | 9 | Shared sokol includes (sokol_log, sokol_glue) |
| shims/win32/shellapi.h | 0 | Empty stub header |
| shims/win32/windowsx.h | 0 | Empty stub header |

---

## Function Manifest

### main.c

| Function | Signature | Line |
|----------|-----------|------|
| `init` | `void init(void)` | 26 |
| `frame` | `void frame(void)` | 49 |
| `cleanup` | `void cleanup(void)` | 87 |
| `input` | `void input(const sapp_event* event)` | 92 |
| `main` | `int main(int argc, char* argv[])` | 96 |

---

### win32_tweaks.c

| Function | Signature | Line |
|----------|-----------|------|
| `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` | 4 |

---

### win32_tweaks.h

| Function | Signature | Line |
|----------|-----------|------|
| `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` | 5 |

---

### nvapi/nvapi.c

| Function | Signature | Line |
|----------|-----------|------|
| `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` | 37 |

---

### nvapi/nvapi.h

| Function | Signature | Line |
|----------|-----------|------|
| `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` | 7 |

---

### shims/linux/x11.c

| Function | Signature | Line |
|----------|-----------|------|
| `load_X11_procs` | `static void load_X11_procs(void)` | 87 |
| `load_Xcursor_procs` | `static void load_Xcursor_procs(void)` | 177 |
| `load_Xi_procs` | `static void load_Xi_procs(void)` | 190 |
| `XOpenDisplay` | `Display * XOpenDisplay(const char* display_name)` | 198 |
| `XCloseDisplay` | `int XCloseDisplay(Display* display)` | 204 |
| `XFlush` | `int XFlush(Display* display)` | 210 |
| `XNextEvent` | `int XNextEvent(Display* display, XEvent* event_return)` | 216 |
| `XPending` | `int XPending(Display* display)` | 222 |
| `XInitThreads` | `Status XInitThreads(void)` | 228 |
| `XFilterEvent` | `Bool XFilterEvent(XEvent* event, Window w)` | 234 |
| `XkbSetDetectableAutoRepeat` | `Bool XkbSetDetectableAutoRepeat(Display* display, Bool detectable, Bool* supported_rtrn)` | 240 |
| `XSync` | `int XSync(Display* display, Bool discard)` | 246 |
| `XrmInitialize` | `void XrmInitialize(void)` | 252 |
| `XChangeProperty` | `int XChangeProperty(Display* display, Window w, Atom property, Atom type, int format, int mode, const unsigned char* data, int nelements)` | 258 |
| `XSendEvent` | `Status XSendEvent(Display* display, Window w, Bool propagate, long event_mask, XEvent* event_send)` | 264 |
| `XFree` | `int XFree(void* data)` | 270 |
| `XSetErrorHandler` | `XErrorHandler XSetErrorHandler(XErrorHandler handler)` | 276 |
| `XConvertSelection` | `int XConvertSelection(Display* display, Atom selection, Atom target, Atom property, Window requestor, Time time)` | 282 |
| `XLookupString` | `int XLookupString(XKeyEvent* event_struct, char* buffer_return, int bytes_buffer, KeySym* keysym_return, XComposeStatus* status_in_out)` | 288 |
| `XGetEventData` | `Bool XGetEventData(Display* display, XGenericEventCookie* cookie)` | 294 |
| `XFreeEventData` | `void XFreeEventData(Display* display, XGenericEventCookie* cookie)` | 300 |
| `XGetWindowProperty` | `int XGetWindowProperty(Display* display, Window w, Atom property, long long_offset, long long_length, Bool delete, Atom req_type, Atom* actual_type_return, int* actual_format_return, unsigned long* nitems_return, unsigned long* bytes_after_return, unsigned char** prop_return)` | 306 |
| `XMapWindow` | `int XMapWindow(Display* display, Window w)` | 312 |
| `XUnmapWindow` | `int XUnmapWindow(Display* display, Window w)` | 318 |
| `XRaiseWindow` | `int XRaiseWindow(Display* display, Window w)` | 324 |
| `XGetWindowAttributes` | `Status XGetWindowAttributes(Display* display, Window w, XWindowAttributes* window_attributes_return)` | 330 |
| `XAllocSizeHints` | `XSizeHints * XAllocSizeHints(void)` | 336 |
| `XCheckTypedWindowEvent` | `Bool XCheckTypedWindowEvent(Display* display, Window w, int event_type, XEvent* event_return)` | 342 |
| `XCreateColormap` | `Colormap XCreateColormap(Display* display, Window w, Visual* visual, int alloc)` | 348 |
| `XCreateFontCursor` | `Cursor XCreateFontCursor(Display* display, unsigned int shape)` | 354 |
| `XCreateWindow` | `Window XCreateWindow(Display* display, Window parent, int x, int y, unsigned int width, unsigned int height, unsigned int border_width, int depth, unsigned int class, Visual* visual, unsigned long valuemask, XSetWindowAttributes* attributes)` | 360 |
| `XWarpPointer` | `int XWarpPointer(Display* display, Window src_w, Window dest_w, int src_x, int src_y, unsigned int src_width, unsigned int src_height, int dest_x, int dest_y)` | 366 |
| `XDefineCursor` | `int XDefineCursor(Display* display, Window w, Cursor cursor)` | 372 |
| `XDestroyWindow` | `int XDestroyWindow(Display* display, Window w)` | 378 |
| `XFreeColormap` | `int XFreeColormap(Display* display, Colormap colormap)` | 384 |
| `XFreeCursor` | `int XFreeCursor(Display* display, Cursor cursor)` | 390 |
| `XGetKeyboardMapping` | `KeySym * XGetKeyboardMapping(Display* display, unsigned int first_keycode, int keycode_count, int* keysyms_per_keycode_return)` | 396 |
| `XGetSelectionOwner` | `Window XGetSelectionOwner(Display* display, Atom selection)` | 402 |
| `XGrabPointer` | `int XGrabPointer(Display* display, Window grab_window, Bool owner_events, unsigned int event_mask, int pointer_mode, int keyboard_mode, Window confine_to, Cursor cursor, Time time)` | 408 |
| `XInternAtom` | `Atom XInternAtom(Display* display, const char* atom_name, Bool only_if_exists)` | 414 |
| `XInternAtoms` | `Status XInternAtoms(Display* display, char** names, int count, Bool only_if_exists, Atom* atoms_return)` | 420 |
| `XSetSelectionOwner` | `int XSetSelectionOwner(Display* display, Atom selection, Window owner, Time time)` | 426 |
| `XSetWMNormalHints` | `void XSetWMNormalHints(Display* display, Window w, XSizeHints* hints)` | 432 |
| `XSetWMProtocols` | `Status XSetWMProtocols(Display* display, Window w, Atom* protocols, int count)` | 438 |
| `XUndefineCursor` | `int XUndefineCursor(Display* display, Window w)` | 444 |
| `XUngrabPointer` | `int XUngrabPointer(Display* display, Time time)` | 450 |
| `Xutf8SetWMProperties` | `void Xutf8SetWMProperties(Display* display, Window w, const char* window_name, const char* icon_name, char** argv, int argc, XSizeHints* normal_hints, XWMHints* wm_hints, XClassHint* class_hints)` | 456 |
| `XkbFreeKeyboard` | `void XkbFreeKeyboard(XkbDescPtr xkb, unsigned int which, Bool free_all)` | 462 |
| `XkbFreeNames` | `void XkbFreeNames(XkbDescPtr xkb, unsigned int which, Bool free_map)` | 468 |
| `XResourceManagerString` | `char * XResourceManagerString(Display* display)` | 474 |
| `XrmDestroyDatabase` | `void XrmDestroyDatabase(XrmDatabase database)` | 480 |
| `XrmGetResource` | `Bool XrmGetResource(XrmDatabase database, const char* str_name, const char* str_class, char** str_type_return, XrmValue* value_return)` | 486 |
| `XkbGetMap` | `XkbDescPtr XkbGetMap(Display* display, unsigned int which, unsigned int device_spec)` | 492 |
| `XkbGetNames` | `Status XkbGetNames(Display* dpy, unsigned int which, XkbDescPtr xkb)` | 498 |
| `XrmGetStringDatabase` | `XrmDatabase XrmGetStringDatabase(const char* data)` | 504 |
| `XQueryExtension` | `Bool XQueryExtension(Display* display, const char* name, int* major_opcode_return, int* first_event_return, int* first_error_return)` | 510 |
| `XcursorGetDefaultSize` | `int XcursorGetDefaultSize(Display* dpy)` | 516 |
| `XcursorGetTheme` | `char * XcursorGetTheme(Display* dpy)` | 522 |
| `XcursorImageCreate` | `XcursorImage * XcursorImageCreate(int width, int height)` | 528 |
| `XcursorImageDestroy` | `void XcursorImageDestroy(XcursorImage* image)` | 534 |
| `XcursorImageLoadCursor` | `Cursor XcursorImageLoadCursor(Display* dpy, const XcursorImage* image)` | 540 |
| `XcursorLibraryLoadImage` | `XcursorImage * XcursorLibraryLoadImage(const char* library, const char* theme, int size)` | 546 |
| `XIQueryVersion` | `Status XIQueryVersion(Display* dpy, int* major_version_inout, int* minor_version_inout)` | 552 |
| `XISelectEvents` | `int XISelectEvents(Display* dpy, Window win, XIEventMask* masks, int num_masks)` | 558 |

---

### shims/linux/gl.c

This file contains **~600 OpenGL function shims** loaded via `cosmo_dlopen("libgl.so")`. Each GL function follows this pattern:

```c
static void (*proc_glFunctionName)(args) = NULL;  // Line ~N
...
void glFunctionName(args) {                        // Line ~N+1000
    if (libgl == NULL) { load_gl_shims(); }
    proc_glFunctionName(args);
}
```

| Function | Signature | Line |
|----------|-----------|------|
| `load_gl_shims` | `static void load_gl_shims(void)` | 768 |

**Sample GL Wrapper Functions (pattern repeated ~600 times):**

| Function | Line (approx) |
|----------|---------------|
| `glAccum` | 1825 |
| `glActiveTexture` | 1831 |
| `glAttachShader` | 1855 |
| `glBegin` | 1861 |
| `glBindBuffer` | 1879 |
| `glBindTexture` | 1897 |
| `glBlendFunc` | 1927 |
| `glBufferData` | 1945 |
| `glClear` | 1969 |
| `glClearColor` | 1993 |
| `glCompileShader` | 2101 |
| `glCreateProgram` | 2155 |
| `glCreateShader` | 2161 |
| `glDeleteBuffers` | 2173 |
| `glDeleteProgram` | 2191 |
| `glDeleteShader` | 2209 |
| `glDisable` | 2251 |
| `glDrawArrays` | 2275 |
| `glDrawElements` | 2293 |
| `glEnable` | 2365 |
| `glEnableVertexAttribArray` | 2377 |
| `glGenBuffers` | 2463 |
| `glGenTextures` | 2487 |
| `glGenVertexArrays` | 2499 |
| `glGetAttribLocation` | 2547 |
| `glGetError` | 2595 |
| `glGetProgramInfoLog` | 2685 |
| `glGetProgramiv` | 2691 |
| `glGetShaderInfoLog` | 2739 |
| `glGetShaderiv` | 2751 |
| `glGetString` | 2757 |
| `glGetUniformLocation` | 2805 |
| `glLinkProgram` | 2967 |
| `glShaderSource` | 3417 |
| `glTexImage2D` | 3519 |
| `glTexParameteri` | 3555 |
| `glUniform1f` | 3609 |
| `glUniform1i` | 3621 |
| `glUniform4fv` | 3693 |
| `glUniformMatrix4fv` | 3759 |
| `glUseProgram` | 3843 |
| `glVertexAttribPointer` | 4047 |
| `glViewport` | 4059 |

---

### shims/sokol/sokol_cosmo.c (Runtime Dispatch Layer)

This file provides **~150 dispatcher functions** that route to platform-specific implementations at runtime. Each follows this pattern:

```c
extern RetType linux_function(args);
extern RetType windows_function(args);
extern RetType macos_function(args);
RetType function(args) {
    if (IsLinux()) { return linux_function(args); }
    if (IsWindows()) { return windows_function(args); }
    if (IsXnu()) { return macos_function(args); }
}
```

**sokol_app functions:**

| Function | Signature | Line |
|----------|-----------|------|
| `sapp_isvalid` | `bool sapp_isvalid(void)` | 13 |
| `sapp_width` | `int sapp_width(void)` | 24 |
| `sapp_widthf` | `float sapp_widthf(void)` | 35 |
| `sapp_height` | `int sapp_height(void)` | 46 |
| `sapp_heightf` | `float sapp_heightf(void)` | 57 |
| `sapp_color_format` | `int sapp_color_format(void)` | 68 |
| `sapp_depth_format` | `int sapp_depth_format(void)` | 79 |
| `sapp_sample_count` | `int sapp_sample_count(void)` | 90 |
| `sapp_high_dpi` | `bool sapp_high_dpi(void)` | 101 |
| `sapp_dpi_scale` | `float sapp_dpi_scale(void)` | 112 |
| `sapp_show_keyboard` | `void sapp_show_keyboard(bool show)` | 123 |
| `sapp_keyboard_shown` | `bool sapp_keyboard_shown(void)` | 136 |
| `sapp_is_fullscreen` | `bool sapp_is_fullscreen(void)` | 147 |
| `sapp_toggle_fullscreen` | `void sapp_toggle_fullscreen(void)` | 158 |
| `sapp_show_mouse` | `void sapp_show_mouse(bool show)` | 171 |
| `sapp_mouse_shown` | `bool sapp_mouse_shown(void)` | 184 |
| `sapp_lock_mouse` | `void sapp_lock_mouse(bool lock)` | 195 |
| `sapp_mouse_locked` | `bool sapp_mouse_locked(void)` | 208 |
| `sapp_set_mouse_cursor` | `void sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 219 |
| `sapp_get_mouse_cursor` | `sapp_mouse_cursor sapp_get_mouse_cursor(void)` | 232 |
| `sapp_userdata` | `void* sapp_userdata(void)` | 243 |
| `sapp_query_desc` | `sapp_desc sapp_query_desc(void)` | 254 |
| `sapp_request_quit` | `void sapp_request_quit(void)` | 265 |
| `sapp_cancel_quit` | `void sapp_cancel_quit(void)` | 278 |
| `sapp_quit` | `void sapp_quit(void)` | 291 |
| `sapp_consume_event` | `void sapp_consume_event(void)` | 304 |
| `sapp_frame_count` | `uint64_t sapp_frame_count(void)` | 317 |
| `sapp_frame_duration` | `double sapp_frame_duration(void)` | 328 |
| `sapp_set_clipboard_string` | `void sapp_set_clipboard_string(const char* str)` | 339 |
| `sapp_get_clipboard_string` | `const char* sapp_get_clipboard_string(void)` | 352 |
| `sapp_set_window_title` | `void sapp_set_window_title(const char* str)` | 363 |
| `sapp_set_icon` | `void sapp_set_icon(const sapp_icon_desc* icon_desc)` | 376 |
| `sapp_get_num_dropped_files` | `int sapp_get_num_dropped_files(void)` | 389 |
| `sapp_get_dropped_file_path` | `const char* sapp_get_dropped_file_path(int index)` | 400 |
| `sapp_run` | `void sapp_run(const sapp_desc* desc)` | 411 |
| `sapp_egl_get_display` | `const void* sapp_egl_get_display(void)` | 424 |
| `sapp_egl_get_context` | `const void* sapp_egl_get_context(void)` | 435 |
| `sapp_html5_ask_leave_site` | `void sapp_html5_ask_leave_site(bool ask)` | 446 |
| `sapp_html5_get_dropped_file_size` | `uint32_t sapp_html5_get_dropped_file_size(int index)` | 459 |
| `sapp_html5_fetch_dropped_file` | `void sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 470 |
| `sapp_metal_get_device` | `const void* sapp_metal_get_device(void)` | 483 |
| `sapp_metal_get_current_drawable` | `const void* sapp_metal_get_current_drawable(void)` | 494 |
| `sapp_metal_get_depth_stencil_texture` | `const void* sapp_metal_get_depth_stencil_texture(void)` | 505 |
| `sapp_metal_get_msaa_color_texture` | `const void* sapp_metal_get_msaa_color_texture(void)` | 516 |
| `sapp_macos_get_window` | `const void* sapp_macos_get_window(void)` | 527 |
| `sapp_ios_get_window` | `const void* sapp_ios_get_window(void)` | 538 |
| `sapp_d3d11_get_device` | `const void* sapp_d3d11_get_device(void)` | 549 |
| `sapp_d3d11_get_device_context` | `const void* sapp_d3d11_get_device_context(void)` | 560 |
| `sapp_d3d11_get_swap_chain` | `const void* sapp_d3d11_get_swap_chain(void)` | 571 |
| `sapp_d3d11_get_render_view` | `const void* sapp_d3d11_get_render_view(void)` | 582 |
| `sapp_d3d11_get_resolve_view` | `const void* sapp_d3d11_get_resolve_view(void)` | 593 |
| `sapp_d3d11_get_depth_stencil_view` | `const void* sapp_d3d11_get_depth_stencil_view(void)` | 604 |
| `sapp_win32_get_hwnd` | `const void* sapp_win32_get_hwnd(void)` | 615 |
| `sapp_wgpu_get_device` | `const void* sapp_wgpu_get_device(void)` | 626 |
| `sapp_wgpu_get_render_view` | `const void* sapp_wgpu_get_render_view(void)` | 637 |
| `sapp_wgpu_get_resolve_view` | `const void* sapp_wgpu_get_resolve_view(void)` | 648 |
| `sapp_wgpu_get_depth_stencil_view` | `const void* sapp_wgpu_get_depth_stencil_view(void)` | 659 |
| `sapp_gl_get_framebuffer` | `uint32_t sapp_gl_get_framebuffer(void)` | 670 |
| `sapp_gl_get_major_version` | `int sapp_gl_get_major_version(void)` | 681 |
| `sapp_gl_get_minor_version` | `int sapp_gl_get_minor_version(void)` | 692 |
| `sapp_android_get_native_activity` | `const void* sapp_android_get_native_activity(void)` | 703 |

**sokol_gfx functions:**

| Function | Signature | Line |
|----------|-----------|------|
| `sg_setup` | `void sg_setup(const sg_desc* desc)` | 714 |
| `sg_shutdown` | `void sg_shutdown(void)` | 727 |
| `sg_isvalid` | `bool sg_isvalid(void)` | 740 |
| `sg_reset_state_cache` | `void sg_reset_state_cache(void)` | 751 |
| `sg_install_trace_hooks` | `sg_trace_hooks sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` | 764 |
| `sg_push_debug_group` | `void sg_push_debug_group(const char* name)` | 775 |
| `sg_pop_debug_group` | `void sg_pop_debug_group(void)` | 788 |
| `sg_add_commit_listener` | `bool sg_add_commit_listener(sg_commit_listener listener)` | 801 |
| `sg_remove_commit_listener` | `bool sg_remove_commit_listener(sg_commit_listener listener)` | 812 |
| `sg_make_buffer` | `sg_buffer sg_make_buffer(const sg_buffer_desc* desc)` | 823 |
| `sg_make_image` | `sg_image sg_make_image(const sg_image_desc* desc)` | 834 |
| `sg_make_sampler` | `sg_sampler sg_make_sampler(const sg_sampler_desc* desc)` | 845 |
| `sg_make_shader` | `sg_shader sg_make_shader(const sg_shader_desc* desc)` | 856 |
| `sg_make_pipeline` | `sg_pipeline sg_make_pipeline(const sg_pipeline_desc* desc)` | 867 |
| `sg_make_attachments` | `sg_attachments sg_make_attachments(const sg_attachments_desc* desc)` | 878 |
| `sg_destroy_buffer` | `void sg_destroy_buffer(sg_buffer buf)` | 889 |
| `sg_destroy_image` | `void sg_destroy_image(sg_image img)` | 902 |
| `sg_destroy_sampler` | `void sg_destroy_sampler(sg_sampler smp)` | 915 |
| `sg_destroy_shader` | `void sg_destroy_shader(sg_shader shd)` | 928 |
| `sg_destroy_pipeline` | `void sg_destroy_pipeline(sg_pipeline pip)` | 941 |
| `sg_destroy_attachments` | `void sg_destroy_attachments(sg_attachments atts)` | 954 |
| `sg_update_buffer` | `void sg_update_buffer(sg_buffer buf, const sg_range* data)` | 967 |
| `sg_update_image` | `void sg_update_image(sg_image img, const sg_image_data* data)` | 980 |
| `sg_append_buffer` | `int sg_append_buffer(sg_buffer buf, const sg_range* data)` | 993 |
| `sg_query_buffer_overflow` | `bool sg_query_buffer_overflow(sg_buffer buf)` | 1004 |
| `sg_query_buffer_will_overflow` | `bool sg_query_buffer_will_overflow(sg_buffer buf, size_t size)` | 1015 |
| `sg_begin_pass` | `void sg_begin_pass(const sg_pass* pass)` | 1026 |
| `sg_apply_viewport` | `void sg_apply_viewport(int x, int y, int width, int height, bool origin_top_left)` | 1039 |
| `sg_apply_viewportf` | `void sg_apply_viewportf(float x, float y, float width, float height, bool origin_top_left)` | 1052 |
| `sg_apply_scissor_rect` | `void sg_apply_scissor_rect(int x, int y, int width, int height, bool origin_top_left)` | 1065 |
| `sg_apply_scissor_rectf` | `void sg_apply_scissor_rectf(float x, float y, float width, float height, bool origin_top_left)` | 1078 |
| `sg_apply_pipeline` | `void sg_apply_pipeline(sg_pipeline pip)` | 1091 |
| `sg_apply_bindings` | `void sg_apply_bindings(const sg_bindings* bindings)` | 1104 |
| `sg_apply_uniforms` | `void sg_apply_uniforms(int ub_slot, const sg_range* data)` | 1117 |
| `sg_draw` | `void sg_draw(int base_element, int num_elements, int num_instances)` | 1130 |
| `sg_end_pass` | `void sg_end_pass(void)` | 1143 |
| `sg_commit` | `void sg_commit(void)` | 1156 |
| `sg_query_desc` | `sg_desc sg_query_desc(void)` | 1169 |
| `sg_query_backend` | `sg_backend sg_query_backend(void)` | 1180 |
| `sg_query_features` | `sg_features sg_query_features(void)` | 1191 |
| `sg_query_limits` | `sg_limits sg_query_limits(void)` | 1202 |
| `sg_query_pixelformat` | `sg_pixelformat_info sg_query_pixelformat(sg_pixel_format fmt)` | 1213 |
| `sg_query_row_pitch` | `int sg_query_row_pitch(sg_pixel_format fmt, int width, int row_align_bytes)` | 1224 |
| `sg_query_surface_pitch` | `int sg_query_surface_pitch(sg_pixel_format fmt, int width, int height, int row_align_bytes)` | 1235 |
| `sg_query_buffer_state` | `sg_resource_state sg_query_buffer_state(sg_buffer buf)` | 1246 |
| `sg_query_image_state` | `sg_resource_state sg_query_image_state(sg_image img)` | 1257 |
| `sg_query_sampler_state` | `sg_resource_state sg_query_sampler_state(sg_sampler smp)` | 1733 |
| `sg_query_shader_state` | `sg_resource_state sg_query_shader_state(sg_shader shd)` | 1746 |
| `sg_query_pipeline_state` | `sg_resource_state sg_query_pipeline_state(sg_pipeline pip)` | 1759 |
| `sg_query_attachments_state` | `sg_resource_state sg_query_attachments_state(sg_attachments atts)` | 1772 |

*...and ~70 more sg_* functions continuing through line 3099*

---

### shims/sokol/sokol_macos.c (macOS Stub Implementation)

This file provides **stub implementations** for macOS since Cosmopolitan cannot directly compile Objective-C.

| Function | Signature | Line |
|----------|-----------|------|
| `_macos_not_implemented` | `static void _macos_not_implemented(const char* func)` | 54 |
| `macos_sapp_isvalid` | `bool macos_sapp_isvalid(void)` | 77 |
| `macos_sapp_width` | `int macos_sapp_width(void)` | 81 |
| `macos_sapp_widthf` | `float macos_sapp_widthf(void)` | 85 |
| `macos_sapp_height` | `int macos_sapp_height(void)` | 89 |
| `macos_sapp_heightf` | `float macos_sapp_heightf(void)` | 93 |
| `macos_sapp_color_format` | `int macos_sapp_color_format(void)` | 97 |
| `macos_sapp_depth_format` | `int macos_sapp_depth_format(void)` | 101 |
| `macos_sapp_sample_count` | `int macos_sapp_sample_count(void)` | 105 |
| `macos_sapp_high_dpi` | `bool macos_sapp_high_dpi(void)` | 109 |
| `macos_sapp_dpi_scale` | `float macos_sapp_dpi_scale(void)` | 113 |
| `macos_sapp_show_keyboard` | `void macos_sapp_show_keyboard(bool show)` | 117 |
| `macos_sapp_keyboard_shown` | `bool macos_sapp_keyboard_shown(void)` | 121 |
| `macos_sapp_is_fullscreen` | `bool macos_sapp_is_fullscreen(void)` | 125 |
| `macos_sapp_toggle_fullscreen` | `void macos_sapp_toggle_fullscreen(void)` | 129 |
| `macos_sapp_show_mouse` | `void macos_sapp_show_mouse(bool show)` | 132 |
| `macos_sapp_mouse_shown` | `bool macos_sapp_mouse_shown(void)` | 136 |
| `macos_sapp_lock_mouse` | `void macos_sapp_lock_mouse(bool lock)` | 140 |
| `macos_sapp_mouse_locked` | `bool macos_sapp_mouse_locked(void)` | 144 |
| `macos_sapp_set_mouse_cursor` | `void macos_sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 148 |
| `macos_sapp_get_mouse_cursor` | `sapp_mouse_cursor macos_sapp_get_mouse_cursor(void)` | 152 |
| `macos_sapp_userdata` | `void* macos_sapp_userdata(void)` | 156 |
| `macos_sapp_query_desc` | `sapp_desc macos_sapp_query_desc(void)` | 160 |
| `macos_sapp_request_quit` | `void macos_sapp_request_quit(void)` | 164 |
| `macos_sapp_cancel_quit` | `void macos_sapp_cancel_quit(void)` | 167 |
| `macos_sapp_quit` | `void macos_sapp_quit(void)` | 170 |
| `macos_sapp_consume_event` | `void macos_sapp_consume_event(void)` | 177 |
| `macos_sapp_frame_count` | `uint64_t macos_sapp_frame_count(void)` | 180 |
| `macos_sapp_frame_duration` | `double macos_sapp_frame_duration(void)` | 184 |
| `macos_sapp_set_clipboard_string` | `void macos_sapp_set_clipboard_string(const char* str)` | 188 |
| `macos_sapp_get_clipboard_string` | `const char* macos_sapp_get_clipboard_string(void)` | 192 |
| `macos_sapp_set_window_title` | `void macos_sapp_set_window_title(const char* str)` | 196 |
| `macos_sapp_set_icon` | `void macos_sapp_set_icon(const sapp_icon_desc* icon_desc)` | 200 |
| `macos_sapp_get_num_dropped_files` | `int macos_sapp_get_num_dropped_files(void)` | 204 |
| `macos_sapp_get_dropped_file_path` | `const char* macos_sapp_get_dropped_file_path(int index)` | 208 |
| `macos_sapp_run` | `void macos_sapp_run(const sapp_desc* desc)` | 213 |
| `macos_sg_setup` | `void macos_sg_setup(const sg_desc* desc)` | 271 |
| `macos_sg_shutdown` | `void macos_sg_shutdown(void)` | 278 |
| `macos_sg_isvalid` | `bool macos_sg_isvalid(void)` | 282 |
| `macos_sg_make_buffer` | `sg_buffer macos_sg_make_buffer(const sg_buffer_desc* desc)` | 302 |
| `macos_sg_make_image` | `sg_image macos_sg_make_image(const sg_image_desc* desc)` | 308 |
| `macos_sg_make_sampler` | `sg_sampler macos_sg_make_sampler(const sg_sampler_desc* desc)` | 314 |
| `macos_sg_make_shader` | `sg_shader macos_sg_make_shader(const sg_shader_desc* desc)` | 320 |
| `macos_sg_make_pipeline` | `sg_pipeline macos_sg_make_pipeline(const sg_pipeline_desc* desc)` | 326 |
| `macos_sg_make_attachments` | `sg_attachments macos_sg_make_attachments(const sg_attachments_desc* desc)` | 332 |
| `macos_sg_begin_pass` | `void macos_sg_begin_pass(const sg_pass* pass)` | 368 |
| `macos_sg_apply_pipeline` | `void macos_sg_apply_pipeline(sg_pipeline pip)` | 388 |
| `macos_sg_apply_bindings` | `void macos_sg_apply_bindings(const sg_bindings* bindings)` | 392 |
| `macos_sg_draw` | `void macos_sg_draw(int base_element, int num_elements, int num_instances)` | 401 |
| `macos_sg_end_pass` | `void macos_sg_end_pass(void)` | 408 |
| `macos_sg_commit` | `void macos_sg_commit(void)` | 411 |
| `macos_sg_query_backend` | `sg_backend macos_sg_query_backend(void)` | 418 |

*...and ~100 more macos_sg_* stub functions through line 694*

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Total Source Files** | 18 |
| **Application Functions** | 5 |
| **Win32 Tweaks Functions** | 1 |
| **NVAPI Functions** | 1 |
| **X11 Shim Functions** | 55 |
| **OpenGL Shim Functions** | ~600 |
| **Sokol Dispatch Functions** | ~150 |
| **macOS Stub Functions** | ~120 |
| **Total Unique Functions** | **~930** |

---

## Key Cosmopolitan Integration Points

### 1. Dynamic Library Loading (dlopen shims)
- **File:** `shims/linux/gl.c`, `shims/linux/x11.c`
- **Pattern:** `cosmo_dlopen()` + `cosmo_dlsym()` + `cosmo_dltramp()`
- **Purpose:** Load platform-native OpenGL/X11 libraries at runtime

### 2. Platform Detection & Dispatch
- **File:** `shims/sokol/sokol_cosmo.c`
- **Pattern:** `IsLinux()` / `IsWindows()` / `IsXnu()` runtime checks
- **Purpose:** Route to correct platform implementation

### 3. Function Prefix Namespacing
- **Files:** `sokol_linux.h`, `sokol_windows.h`, `sokol_macos.h`
- **Pattern:** `#define sapp_run linux_sapp_run` (etc.)
- **Purpose:** Compile all platform backends into single binary without symbol conflicts

### 4. Win32 Type Shims
- **File:** `shims/sokol/sokol_windows.c`
- **Purpose:** Provide Windows types (HWND, MSG, WNDCLASS, etc.) compatible with Cosmopolitan's `<windowsesque.h>`

---

*Generated by cosmo agent for Swiss Rounds v4*
