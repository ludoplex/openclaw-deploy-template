# cosmo-sokol Source Manifest

**Domain:** Deployment and Distribution (Binary Verification, Platform Testing, Release Artifacts)  
**Generated:** 2026-02-09  
**Agent:** neteng (Swiss Rounds v4 - Round 1)

---

## Overview

cosmo-sokol is a Cosmopolitan Libc port of the sokol graphics libraries. It produces a single APE (Actually Portable Executable) binary that runs natively on Windows, Linux, and macOS without modification.

### Project Philosophy
- **NO interpreters** - No Python, Node, or other runtime dependencies
- **Pure C** - All tooling compiled with cosmocc into APE binaries
- **Single portable binary** - One executable for all platforms

### Architecture Pattern
The project uses a **runtime dispatch pattern** for cross-platform support:
1. Platform-specific implementations (sokol_windows.c, sokol_linux.c, sokol_macos.c)
2. Function name prefixing via headers (e.g., `sapp_run` → `windows_sapp_run`)
3. Central dispatcher (sokol_cosmo.c) that routes calls based on `IsLinux()`, `IsWindows()`, `IsXnu()`

---

## Source Function Manifest

### Core Application

#### `repo/main.c`
| Function | Signature | Line |
|----------|-----------|------|
| `init` | `void init(void)` | 25 |
| `frame` | `void frame(void)` | 48 |
| `cleanup` | `void cleanup(void)` | 86 |
| `input` | `void input(const sapp_event* event)` | 91 |
| `main` | `int main(int argc, char* argv[])` | 95 |

#### `repo/win32_tweaks.c`
| Function | Signature | Line |
|----------|-----------|------|
| `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` | 4 |

#### `repo/win32_tweaks.h`
| Function | Signature | Line |
|----------|-----------|------|
| `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` (declaration) | 5 |

---

### NVIDIA API Shim

#### `repo/nvapi/nvapi.c`
| Function | Signature | Line |
|----------|-----------|------|
| `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` | 39 |

#### `repo/nvapi/nvapi.h`
| Function | Signature | Line |
|----------|-----------|------|
| `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` (declaration) | 6 |

---

### Sokol Runtime Dispatch

#### `repo/shims/sokol/sokol_cosmo.c`
Auto-generated runtime dispatcher. Contains 115 dispatch functions:

| Function | Signature | Line |
|----------|-----------|------|
| `sapp_isvalid` | `bool sapp_isvalid(void)` | 11 |
| `sapp_width` | `int sapp_width(void)` | 23 |
| `sapp_widthf` | `float sapp_widthf(void)` | 35 |
| `sapp_height` | `int sapp_height(void)` | 47 |
| `sapp_heightf` | `float sapp_heightf(void)` | 59 |
| `sapp_color_format` | `int sapp_color_format(void)` | 71 |
| `sapp_depth_format` | `int sapp_depth_format(void)` | 83 |
| `sapp_sample_count` | `int sapp_sample_count(void)` | 95 |
| `sapp_high_dpi` | `bool sapp_high_dpi(void)` | 107 |
| `sapp_dpi_scale` | `float sapp_dpi_scale(void)` | 119 |
| `sapp_show_keyboard` | `void sapp_show_keyboard(bool show)` | 131 |
| `sapp_keyboard_shown` | `bool sapp_keyboard_shown(void)` | 145 |
| `sapp_is_fullscreen` | `bool sapp_is_fullscreen(void)` | 157 |
| `sapp_toggle_fullscreen` | `void sapp_toggle_fullscreen(void)` | 169 |
| `sapp_show_mouse` | `void sapp_show_mouse(bool show)` | 183 |
| `sapp_mouse_shown` | `bool sapp_mouse_shown(void)` | 197 |
| `sapp_lock_mouse` | `void sapp_lock_mouse(bool lock)` | 209 |
| `sapp_mouse_locked` | `bool sapp_mouse_locked(void)` | 223 |
| `sapp_set_mouse_cursor` | `void sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 235 |
| `sapp_get_mouse_cursor` | `sapp_mouse_cursor sapp_get_mouse_cursor(void)` | 249 |
| `sapp_userdata` | `void* sapp_userdata(void)` | 261 |
| `sapp_query_desc` | `sapp_desc sapp_query_desc(void)` | 273 |
| `sapp_request_quit` | `void sapp_request_quit(void)` | 285 |
| `sapp_cancel_quit` | `void sapp_cancel_quit(void)` | 299 |
| `sapp_quit` | `void sapp_quit(void)` | 313 |
| `sapp_consume_event` | `void sapp_consume_event(void)` | 327 |
| `sapp_frame_count` | `uint64_t sapp_frame_count(void)` | 341 |
| `sapp_frame_duration` | `double sapp_frame_duration(void)` | 353 |
| `sapp_set_clipboard_string` | `void sapp_set_clipboard_string(const char* str)` | 365 |
| `sapp_get_clipboard_string` | `const char* sapp_get_clipboard_string(void)` | 379 |
| `sapp_set_window_title` | `void sapp_set_window_title(const char* str)` | 391 |
| `sapp_set_icon` | `void sapp_set_icon(const sapp_icon_desc* icon_desc)` | 405 |
| `sapp_get_num_dropped_files` | `int sapp_get_num_dropped_files(void)` | 419 |
| `sapp_get_dropped_file_path` | `const char* sapp_get_dropped_file_path(int index)` | 431 |
| `sapp_run` | `void sapp_run(const sapp_desc* desc)` | 443 |
| `sapp_egl_get_display` | `const void* sapp_egl_get_display(void)` | 457 |
| `sapp_egl_get_context` | `const void* sapp_egl_get_context(void)` | 469 |
| `sapp_html5_ask_leave_site` | `void sapp_html5_ask_leave_site(bool ask)` | 481 |
| `sapp_html5_get_dropped_file_size` | `uint32_t sapp_html5_get_dropped_file_size(int index)` | 495 |
| `sapp_html5_fetch_dropped_file` | `void sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 507 |
| `sapp_metal_get_device` | `const void* sapp_metal_get_device(void)` | 521 |
| `sapp_metal_get_current_drawable` | `const void* sapp_metal_get_current_drawable(void)` | 533 |
| `sapp_metal_get_depth_stencil_texture` | `const void* sapp_metal_get_depth_stencil_texture(void)` | 545 |
| `sapp_metal_get_msaa_color_texture` | `const void* sapp_metal_get_msaa_color_texture(void)` | 557 |
| `sapp_macos_get_window` | `const void* sapp_macos_get_window(void)` | 569 |
| `sapp_ios_get_window` | `const void* sapp_ios_get_window(void)` | 581 |
| `sapp_d3d11_get_device` | `const void* sapp_d3d11_get_device(void)` | 593 |
| `sapp_d3d11_get_device_context` | `const void* sapp_d3d11_get_device_context(void)` | 605 |
| `sapp_d3d11_get_swap_chain` | `const void* sapp_d3d11_get_swap_chain(void)` | 617 |
| `sapp_d3d11_get_render_view` | `const void* sapp_d3d11_get_render_view(void)` | 629 |
| `sapp_d3d11_get_resolve_view` | `const void* sapp_d3d11_get_resolve_view(void)` | 641 |
| `sapp_d3d11_get_depth_stencil_view` | `const void* sapp_d3d11_get_depth_stencil_view(void)` | 653 |
| `sapp_win32_get_hwnd` | `const void* sapp_win32_get_hwnd(void)` | 665 |
| `sapp_wgpu_get_device` | `const void* sapp_wgpu_get_device(void)` | 677 |
| `sapp_wgpu_get_render_view` | `const void* sapp_wgpu_get_render_view(void)` | 689 |
| `sapp_wgpu_get_resolve_view` | `const void* sapp_wgpu_get_resolve_view(void)` | 701 |
| `sapp_wgpu_get_depth_stencil_view` | `const void* sapp_wgpu_get_depth_stencil_view(void)` | 713 |
| `sapp_gl_get_framebuffer` | `uint32_t sapp_gl_get_framebuffer(void)` | 725 |
| `sapp_gl_get_major_version` | `int sapp_gl_get_major_version(void)` | 737 |
| `sapp_gl_get_minor_version` | `int sapp_gl_get_minor_version(void)` | 749 |
| `sapp_android_get_native_activity` | `const void* sapp_android_get_native_activity(void)` | 761 |
| `sg_setup` | `void sg_setup(const sg_desc* desc)` | 773 |
| `sg_shutdown` | `void sg_shutdown(void)` | 787 |
| `sg_isvalid` | `bool sg_isvalid(void)` | 801 |
| `sg_reset_state_cache` | `void sg_reset_state_cache(void)` | 813 |
| `sg_install_trace_hooks` | `sg_trace_hooks sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` | 827 |
| `sg_push_debug_group` | `void sg_push_debug_group(const char* name)` | 839 |
| `sg_pop_debug_group` | `void sg_pop_debug_group(void)` | 853 |
| `sg_add_commit_listener` | `bool sg_add_commit_listener(sg_commit_listener listener)` | 867 |
| `sg_remove_commit_listener` | `bool sg_remove_commit_listener(sg_commit_listener listener)` | 879 |
| `sg_make_buffer` | `sg_buffer sg_make_buffer(const sg_buffer_desc* desc)` | 891 |
| `sg_make_image` | `sg_image sg_make_image(const sg_image_desc* desc)` | 903 |
| `sg_make_sampler` | `sg_sampler sg_make_sampler(const sg_sampler_desc* desc)` | 915 |
| `sg_make_shader` | `sg_shader sg_make_shader(const sg_shader_desc* desc)` | 927 |
| `sg_make_pipeline` | `sg_pipeline sg_make_pipeline(const sg_pipeline_desc* desc)` | 939 |
| `sg_make_attachments` | `sg_attachments sg_make_attachments(const sg_attachments_desc* desc)` | 951 |
| `sg_destroy_buffer` | `void sg_destroy_buffer(sg_buffer buf)` | 963 |
| `sg_destroy_image` | `void sg_destroy_image(sg_image img)` | 977 |
| `sg_destroy_sampler` | `void sg_destroy_sampler(sg_sampler smp)` | 991 |
| `sg_destroy_shader` | `void sg_destroy_shader(sg_shader shd)` | 1005 |
| `sg_destroy_pipeline` | `void sg_destroy_pipeline(sg_pipeline pip)` | 1019 |
| `sg_destroy_attachments` | `void sg_destroy_attachments(sg_attachments atts)` | 1033 |
| `sg_update_buffer` | `void sg_update_buffer(sg_buffer buf, const sg_range* data)` | 1047 |
| `sg_update_image` | `void sg_update_image(sg_image img, const sg_image_data* data)` | 1061 |
| `sg_append_buffer` | `int sg_append_buffer(sg_buffer buf, const sg_range* data)` | 1075 |
| `sg_query_buffer_overflow` | `bool sg_query_buffer_overflow(sg_buffer buf)` | 1087 |
| `sg_query_buffer_will_overflow` | `bool sg_query_buffer_will_overflow(sg_buffer buf, size_t size)` | 1099 |
| `sg_begin_pass` | `void sg_begin_pass(const sg_pass* pass)` | 1111 |
| `sg_apply_viewport` | `void sg_apply_viewport(int x, int y, int width, int height, bool origin_top_left)` | 1125 |
| `sg_apply_viewportf` | `void sg_apply_viewportf(float x, float y, float width, float height, bool origin_top_left)` | 1139 |
| `sg_apply_scissor_rect` | `void sg_apply_scissor_rect(int x, int y, int width, int height, bool origin_top_left)` | 1153 |
| `sg_apply_scissor_rectf` | `void sg_apply_scissor_rectf(float x, float y, float width, float height, bool origin_top_left)` | 1167 |
| `sg_apply_pipeline` | `void sg_apply_pipeline(sg_pipeline pip)` | 1181 |
| `sg_apply_bindings` | `void sg_apply_bindings(const sg_bindings* bindings)` | 1195 |
| `sg_apply_uniforms` | `void sg_apply_uniforms(int ub_slot, const sg_range* data)` | 1209 |
| `sg_draw` | `void sg_draw(int base_element, int num_elements, int num_instances)` | 1223 |
| `sg_end_pass` | `void sg_end_pass(void)` | 1237 |
| `sg_commit` | `void sg_commit(void)` | 1251 |
| `sg_query_desc` | `sg_desc sg_query_desc(void)` | 1265 |
| `sg_query_backend` | `sg_backend sg_query_backend(void)` | 1277 |
| `sg_query_features` | `sg_features sg_query_features(void)` | 1289 |
| `sg_query_limits` | `sg_limits sg_query_limits(void)` | 1301 |
| `sg_query_pixelformat` | `sg_pixelformat_info sg_query_pixelformat(sg_pixel_format fmt)` | 1313 |
| `sg_query_row_pitch` | `int sg_query_row_pitch(sg_pixel_format fmt, int width, int row_align_bytes)` | 1325 |
| `sg_query_surface_pitch` | `int sg_query_surface_pitch(sg_pixel_format fmt, int width, int height, int row_align_bytes)` | 1337 |
| `sg_query_buffer_state` | `sg_resource_state sg_query_buffer_state(sg_buffer buf)` | 1349 |
| `sg_query_image_state` | `sg_resource_state sg_query_image_state(sg_image img)` | 1719 |
| `sg_query_sampler_state` | `sg_resource_state sg_query_sampler_state(sg_sampler smp)` | 1733 |
| `sg_query_shader_state` | `sg_resource_state sg_query_shader_state(sg_shader shd)` | 1747 |
| `sg_query_pipeline_state` | `sg_resource_state sg_query_pipeline_state(sg_pipeline pip)` | 1761 |
| `sg_query_attachments_state` | `sg_resource_state sg_query_attachments_state(sg_attachments atts)` | 1775 |
| `sg_query_buffer_info` | `sg_buffer_info sg_query_buffer_info(sg_buffer buf)` | 1789 |
| `sg_query_image_info` | `sg_image_info sg_query_image_info(sg_image img)` | 1803 |
| `sg_query_sampler_info` | `sg_sampler_info sg_query_sampler_info(sg_sampler smp)` | 1817 |
| `sg_query_shader_info` | `sg_shader_info sg_query_shader_info(sg_shader shd)` | 1831 |
| `sg_query_pipeline_info` | `sg_pipeline_info sg_query_pipeline_info(sg_pipeline pip)` | 1845 |
| `sg_query_attachments_info` | `sg_attachments_info sg_query_attachments_info(sg_attachments atts)` | 1859 |

*(Additional sg_* functions continue in same pattern through line 3099)*

---

### Platform-Specific Backends

#### `repo/shims/sokol/sokol_macos.c`
Stub implementation for macOS (requires ObjC runtime for full impl):

| Function | Signature | Line |
|----------|-----------|------|
| `_macos_not_implemented` | `static void _macos_not_implemented(const char* func)` | 53 |
| `macos_sapp_isvalid` | `bool macos_sapp_isvalid(void)` | 73 |
| `macos_sapp_width` | `int macos_sapp_width(void)` | 77 |
| `macos_sapp_widthf` | `float macos_sapp_widthf(void)` | 81 |
| `macos_sapp_height` | `int macos_sapp_height(void)` | 85 |
| `macos_sapp_heightf` | `float macos_sapp_heightf(void)` | 89 |
| `macos_sapp_color_format` | `int macos_sapp_color_format(void)` | 93 |
| `macos_sapp_depth_format` | `int macos_sapp_depth_format(void)` | 97 |
| `macos_sapp_sample_count` | `int macos_sapp_sample_count(void)` | 101 |
| `macos_sapp_high_dpi` | `bool macos_sapp_high_dpi(void)` | 105 |
| `macos_sapp_dpi_scale` | `float macos_sapp_dpi_scale(void)` | 109 |
| `macos_sapp_show_keyboard` | `void macos_sapp_show_keyboard(bool show)` | 113 |
| `macos_sapp_keyboard_shown` | `bool macos_sapp_keyboard_shown(void)` | 117 |
| `macos_sapp_is_fullscreen` | `bool macos_sapp_is_fullscreen(void)` | 121 |
| `macos_sapp_toggle_fullscreen` | `void macos_sapp_toggle_fullscreen(void)` | 125 |
| `macos_sapp_show_mouse` | `void macos_sapp_show_mouse(bool show)` | 128 |
| `macos_sapp_mouse_shown` | `bool macos_sapp_mouse_shown(void)` | 132 |
| `macos_sapp_lock_mouse` | `void macos_sapp_lock_mouse(bool lock)` | 136 |
| `macos_sapp_mouse_locked` | `bool macos_sapp_mouse_locked(void)` | 140 |
| `macos_sapp_set_mouse_cursor` | `void macos_sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 144 |
| `macos_sapp_get_mouse_cursor` | `sapp_mouse_cursor macos_sapp_get_mouse_cursor(void)` | 148 |
| `macos_sapp_userdata` | `void* macos_sapp_userdata(void)` | 152 |
| `macos_sapp_query_desc` | `sapp_desc macos_sapp_query_desc(void)` | 156 |
| `macos_sapp_request_quit` | `void macos_sapp_request_quit(void)` | 160 |
| `macos_sapp_cancel_quit` | `void macos_sapp_cancel_quit(void)` | 163 |
| `macos_sapp_quit` | `void macos_sapp_quit(void)` | 166 |
| `macos_sapp_consume_event` | `void macos_sapp_consume_event(void)` | 173 |
| `macos_sapp_frame_count` | `uint64_t macos_sapp_frame_count(void)` | 176 |
| `macos_sapp_frame_duration` | `double macos_sapp_frame_duration(void)` | 180 |
| `macos_sapp_set_clipboard_string` | `void macos_sapp_set_clipboard_string(const char* str)` | 184 |
| `macos_sapp_get_clipboard_string` | `const char* macos_sapp_get_clipboard_string(void)` | 188 |
| `macos_sapp_set_window_title` | `void macos_sapp_set_window_title(const char* str)` | 192 |
| `macos_sapp_set_icon` | `void macos_sapp_set_icon(const sapp_icon_desc* icon_desc)` | 196 |
| `macos_sapp_get_num_dropped_files` | `int macos_sapp_get_num_dropped_files(void)` | 200 |
| `macos_sapp_get_dropped_file_path` | `const char* macos_sapp_get_dropped_file_path(int index)` | 204 |
| `macos_sapp_run` | `void macos_sapp_run(const sapp_desc* desc)` | 209 |
| `macos_sg_setup` | `void macos_sg_setup(const sg_desc* desc)` | 280 |
| `macos_sg_shutdown` | `void macos_sg_shutdown(void)` | 287 |
| `macos_sg_isvalid` | `bool macos_sg_isvalid(void)` | 291 |

*(115 total macos_* stub functions defined through line 718)*

---

### Linux System Shims

#### `repo/shims/linux/x11.c`
Dynamic library loading for X11:

| Function | Signature | Line |
|----------|-----------|------|
| `load_X11_procs` | `static void load_X11_procs(void)` | 80 |
| `load_Xcursor_procs` | `static void load_Xcursor_procs(void)` | 152 |
| `load_Xi_procs` | `static void load_Xi_procs(void)` | 168 |
| `XOpenDisplay` | `Display * XOpenDisplay(const char* display_name)` | 175 |
| `XCloseDisplay` | `int XCloseDisplay(Display* display)` | 181 |
| `XFlush` | `int XFlush(Display* display)` | 187 |
| `XNextEvent` | `int XNextEvent(Display* display, XEvent* event_return)` | 193 |
| `XPending` | `int XPending(Display* display)` | 199 |
| `XInitThreads` | `Status XInitThreads(void)` | 205 |
| `XFilterEvent` | `Bool XFilterEvent(XEvent* event, Window w)` | 211 |
| `XkbSetDetectableAutoRepeat` | `Bool XkbSetDetectableAutoRepeat(Display* display, Bool detectable, Bool* supported_rtrn)` | 217 |
| `XSync` | `int XSync(Display* display, Bool discard)` | 223 |
| `XrmInitialize` | `void XrmInitialize(void)` | 229 |
| `XChangeProperty` | `int XChangeProperty(Display* display, Window w, Atom property, Atom type, int format, int mode, const unsigned char* data, int nelements)` | 235 |
| `XSendEvent` | `Status XSendEvent(Display* display, Window w, Bool propagate, long event_mask, XEvent* event_send)` | 241 |
| `XFree` | `int XFree(void* data)` | 247 |
| `XSetErrorHandler` | `XErrorHandler XSetErrorHandler(XErrorHandler handler)` | 253 |
| `XConvertSelection` | `int XConvertSelection(Display* display, Atom selection, Atom target, Atom property, Window requestor, Time time)` | 259 |
| `XLookupString` | `int XLookupString(XKeyEvent* event_struct, char* buffer_return, int bytes_buffer, KeySym* keysym_return, XComposeStatus* status_in_out)` | 265 |
| `XGetEventData` | `Bool XGetEventData(Display* display, XGenericEventCookie* cookie)` | 271 |
| `XFreeEventData` | `void XFreeEventData(Display* display, XGenericEventCookie* cookie)` | 277 |
| `XGetWindowProperty` | `int XGetWindowProperty(...)` | 283 |
| `XMapWindow` | `int XMapWindow(Display* display, Window w)` | 289 |
| `XUnmapWindow` | `int XUnmapWindow(Display* display, Window w)` | 295 |
| `XRaiseWindow` | `int XRaiseWindow(Display* display, Window w)` | 301 |
| `XGetWindowAttributes` | `Status XGetWindowAttributes(Display* display, Window w, XWindowAttributes* window_attributes_return)` | 307 |
| `XAllocSizeHints` | `XSizeHints * XAllocSizeHints(void)` | 313 |
| `XCheckTypedWindowEvent` | `Bool XCheckTypedWindowEvent(Display* display, Window w, int event_type, XEvent* event_return)` | 319 |
| `XCreateColormap` | `Colormap XCreateColormap(Display* display, Window w, Visual* visual, int alloc)` | 325 |
| `XCreateFontCursor` | `Cursor XCreateFontCursor(Display* display, unsigned int shape)` | 331 |
| `XCreateWindow` | `Window XCreateWindow(...)` | 337 |
| `XWarpPointer` | `int XWarpPointer(...)` | 343 |
| `XDefineCursor` | `int XDefineCursor(Display* display, Window w, Cursor cursor)` | 349 |
| `XDestroyWindow` | `int XDestroyWindow(Display* display, Window w)` | 355 |
| `XFreeColormap` | `int XFreeColormap(Display* display, Colormap colormap)` | 361 |
| `XFreeCursor` | `int XFreeCursor(Display* display, Cursor cursor)` | 367 |
| `XGetKeyboardMapping` | `KeySym * XGetKeyboardMapping(...)` | 373 |
| `XGetSelectionOwner` | `Window XGetSelectionOwner(Display* display, Atom selection)` | 379 |
| `XGrabPointer` | `int XGrabPointer(...)` | 385 |
| `XInternAtom` | `Atom XInternAtom(Display* display, const char* atom_name, Bool only_if_exists)` | 391 |
| `XInternAtoms` | `Status XInternAtoms(Display* display, char** names, int count, Bool only_if_exists, Atom* atoms_return)` | 397 |
| `XSetSelectionOwner` | `int XSetSelectionOwner(Display* display, Atom selection, Window owner, Time time)` | 403 |
| `XSetWMNormalHints` | `void XSetWMNormalHints(Display* display, Window w, XSizeHints* hints)` | 409 |
| `XSetWMProtocols` | `Status XSetWMProtocols(Display* display, Window w, Atom* protocols, int count)` | 415 |
| `XUndefineCursor` | `int XUndefineCursor(Display* display, Window w)` | 421 |
| `XUngrabPointer` | `int XUngrabPointer(Display* display, Time time)` | 427 |
| `Xutf8SetWMProperties` | `void Xutf8SetWMProperties(...)` | 433 |
| `XkbFreeKeyboard` | `void XkbFreeKeyboard(XkbDescPtr xkb, unsigned int which, Bool free_all)` | 439 |
| `XkbFreeNames` | `void XkbFreeNames(XkbDescPtr xkb, unsigned int which, Bool free_map)` | 445 |
| `XResourceManagerString` | `char * XResourceManagerString(Display* display)` | 451 |
| `XrmDestroyDatabase` | `void XrmDestroyDatabase(XrmDatabase database)` | 457 |
| `XrmGetResource` | `Bool XrmGetResource(XrmDatabase database, const char* str_name, const char* str_class, char** str_type_return, XrmValue* value_return)` | 463 |
| `XkbGetMap` | `XkbDescPtr XkbGetMap(Display* display, unsigned int which, unsigned int device_spec)` | 469 |
| `XkbGetNames` | `Status XkbGetNames(Display* dpy, unsigned int which, XkbDescPtr xkb)` | 475 |
| `XrmGetStringDatabase` | `XrmDatabase XrmGetStringDatabase(const char* data)` | 481 |
| `XQueryExtension` | `Bool XQueryExtension(Display* display, const char* name, int* major_opcode_return, int* first_event_return, int* first_error_return)` | 487 |
| `XcursorGetDefaultSize` | `int XcursorGetDefaultSize(Display* dpy)` | 493 |
| `XcursorGetTheme` | `char * XcursorGetTheme(Display* dpy)` | 499 |
| `XcursorImageCreate` | `XcursorImage * XcursorImageCreate(int width, int height)` | 505 |
| `XcursorImageDestroy` | `void XcursorImageDestroy(XcursorImage* image)` | 511 |
| `XcursorImageLoadCursor` | `Cursor XcursorImageLoadCursor(Display* dpy, const XcursorImage* image)` | 517 |
| `XcursorLibraryLoadImage` | `XcursorImage * XcursorLibraryLoadImage(const char* library, const char* theme, int size)` | 523 |
| `XIQueryVersion` | `Status XIQueryVersion(Display* dpy, int* major_version_inout, int* minor_version_inout)` | 529 |
| `XISelectEvents` | `int XISelectEvents(Display* dpy, Window win, XIEventMask* masks, int num_masks)` | 535 |

#### `repo/shims/linux/gl.c`
OpenGL function loader (6173 lines total):

| Function | Signature | Line |
|----------|-----------|------|
| `load_gl_procs` | `static void load_gl_procs(void)` | ~500 |
| `glAccum` | `void glAccum(GLenum op, GLfloat value)` | (dynamically loaded) |
| `glActiveTexture` | `void glActiveTexture(GLenum texture)` | (dynamically loaded) |

*(547 OpenGL wrapper functions following the same pattern)*

---

## Summary Statistics

| Category | Files | Functions |
|----------|-------|-----------|
| Core Application | 4 | 7 |
| Sokol Dispatch | 1 | 115 |
| macOS Stubs | 1 | 115 |
| Linux Platform Headers | 2 | 115 |
| Windows Platform Headers | 2 | 115 |
| X11 Shim | 1 | 65 |
| OpenGL Shim | 1 | ~547 |
| NVAPI | 2 | 1 |
| **Total** | **~14** | **~1,080** |

---

## Build System

### Build Script: `repo/build`
Shell script that:
1. Compiles platform-specific backends (`sokol_windows.c`, `sokol_linux.c`, `sokol_macos.c`)
2. Compiles shared sokol code and dispatcher
3. Compiles Dear ImGui (cimgui)
4. Compiles platform shims (X11, OpenGL for Linux)
5. Links with `cosmoc++` to produce `bin/cosmo-sokol`

### Code Generator: `repo/shims/sokol/gen-sokol` (Python - VIOLATES PROJECT PHILOSOPHY!)
⚠️ **NOTE:** This generator script is Python, which violates the project philosophy of "NO interpreters". This should be rewritten as a C tool compiled with cosmocc.

---

## Platform Support Status

| Platform | Status | Notes |
|----------|--------|-------|
| **Windows** | ✅ Full | Native Win32/OpenGL via sokol |
| **Linux** | ✅ Full | X11/OpenGL via dynamic shims |
| **macOS** | ⚠️ Stub | Requires ObjC runtime implementation |

---

## Deployment Recommendations

1. **Binary Verification**
   - SHA256 checksums for release artifacts
   - Test on all three platforms before release

2. **Platform Testing**
   - Windows: Direct execution
   - Linux: Verify X11 libraries available (libX11, libXcursor, libXi)
   - macOS: Currently outputs error message (stub)

3. **Release Artifacts**
   - Single `cosmo-sokol` APE binary
   - README with platform-specific notes
   - LICENSE file

4. **Maintenance Priority**
   - Replace `gen-sokol` Python script with C implementation
   - Implement macOS backend via ObjC runtime from C
