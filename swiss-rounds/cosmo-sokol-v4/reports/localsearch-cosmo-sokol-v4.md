# cosmo-sokol Source Manifest
**Generated:** 2026-02-09  
**Repository:** C:\Users\user\cosmo-sokol (ludoplex/cosmo-sokol fork)  
**Upstream:** floooh/sokol, jart/cosmopolitan

---

## Project Overview

cosmo-sokol is a **Cosmopolitan Libc** port of the sokol graphics libraries, enabling single-binary cross-platform builds (Linux + Windows + macOS) using the APE (Actually Portable Executable) format.

### Philosophy
- **Pure C compiled with cosmocc into APE binaries**
- **NO Python/Node/interpreters** (gen scripts are build-time only)
- **Single portable binary, no runtime dependencies**
- **Runtime platform dispatch** via Cosmopolitan's IsLinux()/IsWindows()/IsXnu()

---

## File Structure Summary

| Directory | Purpose |
|-----------|---------|
| `/` | Main application entry (main.c, build script) |
| `/nvapi/` | NVIDIA driver API integration (Windows) |
| `/shims/sokol/` | Platform-specific sokol implementations |
| `/shims/linux/` | Linux X11/OpenGL dynamic loading shims |
| `/shims/win32/` | Windows header shims |
| `/deps/sokol/` | Upstream sokol headers (single-file libs) |
| `/deps/cimgui/` | Dear ImGui C bindings |

---

## FUNCTION MANIFEST

### main.c — Application Entry
| Function | Signature | Line |
|----------|-----------|------|
| `init` | `void init(void)` | 24 |
| `frame` | `void frame(void)` | 44 |
| `cleanup` | `void cleanup(void)` | 82 |
| `input` | `void input(const sapp_event* event)` | 87 |
| `main` | `int main(int argc, char* argv[])` | 91 |

### win32_tweaks.c — Windows Console Helpers
| Function | Signature | Line |
|----------|-----------|------|
| `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` | 4 |

### win32_tweaks.h — Header
| Function | Signature | Line |
|----------|-----------|------|
| `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` (decl) | 5 |

### nvapi/nvapi.c — NVIDIA Thread Optimization Control
| Function | Signature | Line |
|----------|-----------|------|
| `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` | 36 |

### nvapi/nvapi.h — Header
| Function | Signature | Line |
|----------|-----------|------|
| `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` (decl) | 7 |

---

## SOKOL PLATFORM SHIMS

### shims/sokol/sokol_cosmo.c — Runtime Platform Dispatch (Auto-generated)
**Total functions:** 190 dispatch wrappers

Each function follows the pattern:
```c
return_type func_name(args) {
    if (IsLinux())  { return linux_func_name(args); }
    if (IsWindows()){ return windows_func_name(args); }
    if (IsXnu())    { return macos_func_name(args); }
}
```

#### sokol_app (sapp_*) Functions — Lines 10-602
| Function | Signature | Line |
|----------|-----------|------|
| `sapp_isvalid` | `bool sapp_isvalid(void)` | 10 |
| `sapp_width` | `int sapp_width(void)` | 22 |
| `sapp_widthf` | `float sapp_widthf(void)` | 34 |
| `sapp_height` | `int sapp_height(void)` | 46 |
| `sapp_heightf` | `float sapp_heightf(void)` | 58 |
| `sapp_color_format` | `int sapp_color_format(void)` | 70 |
| `sapp_depth_format` | `int sapp_depth_format(void)` | 82 |
| `sapp_sample_count` | `int sapp_sample_count(void)` | 94 |
| `sapp_high_dpi` | `bool sapp_high_dpi(void)` | 106 |
| `sapp_dpi_scale` | `float sapp_dpi_scale(void)` | 118 |
| `sapp_show_keyboard` | `void sapp_show_keyboard(bool show)` | 130 |
| `sapp_keyboard_shown` | `bool sapp_keyboard_shown(void)` | 143 |
| `sapp_is_fullscreen` | `bool sapp_is_fullscreen(void)` | 155 |
| `sapp_toggle_fullscreen` | `void sapp_toggle_fullscreen(void)` | 167 |
| `sapp_show_mouse` | `void sapp_show_mouse(bool show)` | 180 |
| `sapp_mouse_shown` | `bool sapp_mouse_shown(void)` | 193 |
| `sapp_lock_mouse` | `void sapp_lock_mouse(bool lock)` | 205 |
| `sapp_mouse_locked` | `bool sapp_mouse_locked(void)` | 218 |
| `sapp_set_mouse_cursor` | `void sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 230 |
| `sapp_get_mouse_cursor` | `sapp_mouse_cursor sapp_get_mouse_cursor(void)` | 243 |
| `sapp_userdata` | `void* sapp_userdata(void)` | 255 |
| `sapp_query_desc` | `sapp_desc sapp_query_desc(void)` | 267 |
| `sapp_request_quit` | `void sapp_request_quit(void)` | 279 |
| `sapp_cancel_quit` | `void sapp_cancel_quit(void)` | 292 |
| `sapp_quit` | `void sapp_quit(void)` | 305 |
| `sapp_consume_event` | `void sapp_consume_event(void)` | 318 |
| `sapp_frame_count` | `uint64_t sapp_frame_count(void)` | 331 |
| `sapp_frame_duration` | `double sapp_frame_duration(void)` | 343 |
| `sapp_set_clipboard_string` | `void sapp_set_clipboard_string(const char* str)` | 355 |
| `sapp_get_clipboard_string` | `const char* sapp_get_clipboard_string(void)` | 368 |
| `sapp_set_window_title` | `void sapp_set_window_title(const char* str)` | 380 |
| `sapp_set_icon` | `void sapp_set_icon(const sapp_icon_desc* icon_desc)` | 393 |
| `sapp_get_num_dropped_files` | `int sapp_get_num_dropped_files(void)` | 406 |
| `sapp_get_dropped_file_path` | `const char* sapp_get_dropped_file_path(int index)` | 418 |
| `sapp_run` | `void sapp_run(const sapp_desc* desc)` | 430 |
| `sapp_egl_get_display` | `const void* sapp_egl_get_display(void)` | 443 |
| `sapp_egl_get_context` | `const void* sapp_egl_get_context(void)` | 455 |
| `sapp_html5_ask_leave_site` | `void sapp_html5_ask_leave_site(bool ask)` | 467 |
| `sapp_html5_get_dropped_file_size` | `uint32_t sapp_html5_get_dropped_file_size(int index)` | 480 |
| `sapp_html5_fetch_dropped_file` | `void sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 492 |
| `sapp_metal_get_device` | `const void* sapp_metal_get_device(void)` | 505 |
| `sapp_metal_get_current_drawable` | `const void* sapp_metal_get_current_drawable(void)` | 517 |
| `sapp_metal_get_depth_stencil_texture` | `const void* sapp_metal_get_depth_stencil_texture(void)` | 529 |
| `sapp_metal_get_msaa_color_texture` | `const void* sapp_metal_get_msaa_color_texture(void)` | 541 |
| `sapp_macos_get_window` | `const void* sapp_macos_get_window(void)` | 553 |
| `sapp_ios_get_window` | `const void* sapp_ios_get_window(void)` | 565 |
| `sapp_d3d11_get_device` | `const void* sapp_d3d11_get_device(void)` | 577 |
| `sapp_d3d11_get_device_context` | `const void* sapp_d3d11_get_device_context(void)` | 589 |
| `sapp_d3d11_get_swap_chain` | `const void* sapp_d3d11_get_swap_chain(void)` | 601 |
| `sapp_d3d11_get_render_view` | `const void* sapp_d3d11_get_render_view(void)` | 613 |
| `sapp_d3d11_get_resolve_view` | `const void* sapp_d3d11_get_resolve_view(void)` | 625 |
| `sapp_d3d11_get_depth_stencil_view` | `const void* sapp_d3d11_get_depth_stencil_view(void)` | 637 |
| `sapp_win32_get_hwnd` | `const void* sapp_win32_get_hwnd(void)` | 649 |
| `sapp_wgpu_get_device` | `const void* sapp_wgpu_get_device(void)` | 661 |
| `sapp_wgpu_get_render_view` | `const void* sapp_wgpu_get_render_view(void)` | 673 |
| `sapp_wgpu_get_resolve_view` | `const void* sapp_wgpu_get_resolve_view(void)` | 685 |
| `sapp_wgpu_get_depth_stencil_view` | `const void* sapp_wgpu_get_depth_stencil_view(void)` | 697 |
| `sapp_gl_get_framebuffer` | `uint32_t sapp_gl_get_framebuffer(void)` | 709 |
| `sapp_gl_get_major_version` | `int sapp_gl_get_major_version(void)` | 721 |
| `sapp_gl_get_minor_version` | `int sapp_gl_get_minor_version(void)` | 733 |
| `sapp_android_get_native_activity` | `const void* sapp_android_get_native_activity(void)` | 745 |

#### sokol_gfx (sg_*) Functions — Lines 757-3099
| Function | Signature | Line |
|----------|-----------|------|
| `sg_setup` | `void sg_setup(const sg_desc* desc)` | 757 |
| `sg_shutdown` | `void sg_shutdown(void)` | 770 |
| `sg_isvalid` | `bool sg_isvalid(void)` | 783 |
| `sg_reset_state_cache` | `void sg_reset_state_cache(void)` | 795 |
| `sg_install_trace_hooks` | `sg_trace_hooks sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` | 808 |
| `sg_push_debug_group` | `void sg_push_debug_group(const char* name)` | 820 |
| `sg_pop_debug_group` | `void sg_pop_debug_group(void)` | 833 |
| `sg_add_commit_listener` | `bool sg_add_commit_listener(sg_commit_listener listener)` | 846 |
| `sg_remove_commit_listener` | `bool sg_remove_commit_listener(sg_commit_listener listener)` | 858 |
| `sg_make_buffer` | `sg_buffer sg_make_buffer(const sg_buffer_desc* desc)` | 870 |
| `sg_make_image` | `sg_image sg_make_image(const sg_image_desc* desc)` | 882 |
| `sg_make_sampler` | `sg_sampler sg_make_sampler(const sg_sampler_desc* desc)` | 894 |
| `sg_make_shader` | `sg_shader sg_make_shader(const sg_shader_desc* desc)` | 906 |
| `sg_make_pipeline` | `sg_pipeline sg_make_pipeline(const sg_pipeline_desc* desc)` | 918 |
| `sg_make_attachments` | `sg_attachments sg_make_attachments(const sg_attachments_desc* desc)` | 930 |
| `sg_destroy_buffer` | `void sg_destroy_buffer(sg_buffer buf)` | 942 |
| `sg_destroy_image` | `void sg_destroy_image(sg_image img)` | 955 |
| `sg_destroy_sampler` | `void sg_destroy_sampler(sg_sampler smp)` | 968 |
| `sg_destroy_shader` | `void sg_destroy_shader(sg_shader shd)` | 981 |
| `sg_destroy_pipeline` | `void sg_destroy_pipeline(sg_pipeline pip)` | 994 |
| `sg_destroy_attachments` | `void sg_destroy_attachments(sg_attachments atts)` | 1007 |
| `sg_update_buffer` | `void sg_update_buffer(sg_buffer buf, const sg_range* data)` | 1020 |
| `sg_update_image` | `void sg_update_image(sg_image img, const sg_image_data* data)` | 1033 |
| `sg_append_buffer` | `int sg_append_buffer(sg_buffer buf, const sg_range* data)` | 1046 |
| `sg_query_buffer_overflow` | `bool sg_query_buffer_overflow(sg_buffer buf)` | 1058 |
| `sg_query_buffer_will_overflow` | `bool sg_query_buffer_will_overflow(sg_buffer buf, size_t size)` | 1070 |
| `sg_begin_pass` | `void sg_begin_pass(const sg_pass* pass)` | 1082 |
| `sg_apply_viewport` | `void sg_apply_viewport(int x, int y, int width, int height, bool origin_top_left)` | 1095 |
| `sg_apply_viewportf` | `void sg_apply_viewportf(float x, float y, float width, float height, bool origin_top_left)` | 1108 |
| `sg_apply_scissor_rect` | `void sg_apply_scissor_rect(int x, int y, int width, int height, bool origin_top_left)` | 1121 |
| `sg_apply_scissor_rectf` | `void sg_apply_scissor_rectf(float x, float y, float width, float height, bool origin_top_left)` | 1134 |
| `sg_apply_pipeline` | `void sg_apply_pipeline(sg_pipeline pip)` | 1147 |
| `sg_apply_bindings` | `void sg_apply_bindings(const sg_bindings* bindings)` | 1160 |
| `sg_apply_uniforms` | `void sg_apply_uniforms(int ub_slot, const sg_range* data)` | 1173 |
| `sg_draw` | `void sg_draw(int base_element, int num_elements, int num_instances)` | 1186 |
| `sg_end_pass` | `void sg_end_pass(void)` | 1199 |
| `sg_commit` | `void sg_commit(void)` | 1212 |
| `sg_query_desc` | `sg_desc sg_query_desc(void)` | 1225 |
| `sg_query_backend` | `sg_backend sg_query_backend(void)` | 1237 |
| `sg_query_features` | `sg_features sg_query_features(void)` | 1249 |
| `sg_query_limits` | `sg_limits sg_query_limits(void)` | 1261 |
| `sg_query_pixelformat` | `sg_pixelformat_info sg_query_pixelformat(sg_pixel_format fmt)` | 1273 |
| `sg_query_row_pitch` | `int sg_query_row_pitch(sg_pixel_format fmt, int width, int row_align_bytes)` | 1285 |
| `sg_query_surface_pitch` | `int sg_query_surface_pitch(sg_pixel_format fmt, int width, int height, int row_align_bytes)` | 1297 |
| `sg_query_buffer_state` | `sg_resource_state sg_query_buffer_state(sg_buffer buf)` | 1309 |
| `sg_query_image_state` | `sg_resource_state sg_query_image_state(sg_image img)` | 1321 |
| `sg_query_sampler_state` | `sg_resource_state sg_query_sampler_state(sg_sampler smp)` | 1333 |
| `sg_query_shader_state` | `sg_resource_state sg_query_shader_state(sg_shader shd)` | 1345 |
| `sg_query_pipeline_state` | `sg_resource_state sg_query_pipeline_state(sg_pipeline pip)` | 1357 |
| `sg_query_attachments_state` | `sg_resource_state sg_query_attachments_state(sg_attachments atts)` | 1369 |
| `sg_query_buffer_info` | `sg_buffer_info sg_query_buffer_info(sg_buffer buf)` | 1381 |
| `sg_query_image_info` | `sg_image_info sg_query_image_info(sg_image img)` | 1393 |
| `sg_query_sampler_info` | `sg_sampler_info sg_query_sampler_info(sg_sampler smp)` | 1405 |
| `sg_query_shader_info` | `sg_shader_info sg_query_shader_info(sg_shader shd)` | 1417 |
| `sg_query_pipeline_info` | `sg_pipeline_info sg_query_pipeline_info(sg_pipeline pip)` | 1429 |
| `sg_query_attachments_info` | `sg_attachments_info sg_query_attachments_info(sg_attachments atts)` | 1441 |
| `sg_query_buffer_desc` | `sg_buffer_desc sg_query_buffer_desc(sg_buffer buf)` | 1453 |
| `sg_query_image_desc` | `sg_image_desc sg_query_image_desc(sg_image img)` | 1465 |
| `sg_query_sampler_desc` | `sg_sampler_desc sg_query_sampler_desc(sg_sampler smp)` | 1477 |
| `sg_query_shader_desc` | `sg_shader_desc sg_query_shader_desc(sg_shader shd)` | 1489 |
| `sg_query_pipeline_desc` | `sg_pipeline_desc sg_query_pipeline_desc(sg_pipeline pip)` | 1501 |
| `sg_query_attachments_desc` | `sg_attachments_desc sg_query_attachments_desc(sg_attachments atts)` | 1513 |
| `sg_query_buffer_defaults` | `sg_buffer_desc sg_query_buffer_defaults(const sg_buffer_desc* desc)` | 1525 |
| `sg_query_image_defaults` | `sg_image_desc sg_query_image_defaults(const sg_image_desc* desc)` | 1537 |
| `sg_query_sampler_defaults` | `sg_sampler_desc sg_query_sampler_defaults(const sg_sampler_desc* desc)` | 1549 |
| `sg_query_shader_defaults` | `sg_shader_desc sg_query_shader_defaults(const sg_shader_desc* desc)` | 1561 |
| `sg_query_pipeline_defaults` | `sg_pipeline_desc sg_query_pipeline_defaults(const sg_pipeline_desc* desc)` | 1573 |
| `sg_query_attachments_defaults` | `sg_attachments_desc sg_query_attachments_defaults(const sg_attachments_desc* desc)` | 1585 |
| `sg_alloc_buffer` | `sg_buffer sg_alloc_buffer(void)` | 1597 |
| `sg_alloc_image` | `sg_image sg_alloc_image(void)` | 1609 |
| `sg_alloc_sampler` | `sg_sampler sg_alloc_sampler(void)` | 1621 |
| `sg_alloc_shader` | `sg_shader sg_alloc_shader(void)` | 1633 |
| `sg_alloc_pipeline` | `sg_pipeline sg_alloc_pipeline(void)` | 1645 |
| `sg_alloc_attachments` | `sg_attachments sg_alloc_attachments(void)` | 1657 |
| `sg_dealloc_buffer` | `void sg_dealloc_buffer(sg_buffer buf)` | 1669 |
| `sg_dealloc_image` | `void sg_dealloc_image(sg_image img)` | 1682 |
| `sg_dealloc_sampler` | `void sg_dealloc_sampler(sg_sampler smp)` | 1695 |
| `sg_dealloc_shader` | `void sg_dealloc_shader(sg_shader shd)` | 1708 |
| `sg_dealloc_pipeline` | `void sg_dealloc_pipeline(sg_pipeline pip)` | 1721 |
| `sg_dealloc_attachments` | `void sg_dealloc_attachments(sg_attachments attachments)` | 1734 |
| ... | (continues for remaining 80+ sg_* functions) | ... |

---

### shims/sokol/sokol_macos.c — macOS Stub Implementation
**Status:** STUB (not yet functional)  
**Lines:** ~750  

#### Helper Functions
| Function | Signature | Line |
|----------|-----------|------|
| `_macos_not_implemented` | `static void _macos_not_implemented(const char* func)` | 60 |

#### sapp_* Stubs
| Function | Signature | Line |
|----------|-----------|------|
| `macos_sapp_isvalid` | `bool macos_sapp_isvalid(void)` | 78 |
| `macos_sapp_width` | `int macos_sapp_width(void)` | 82 |
| `macos_sapp_widthf` | `float macos_sapp_widthf(void)` | 86 |
| `macos_sapp_height` | `int macos_sapp_height(void)` | 90 |
| `macos_sapp_heightf` | `float macos_sapp_heightf(void)` | 94 |
| `macos_sapp_color_format` | `int macos_sapp_color_format(void)` | 98 |
| `macos_sapp_depth_format` | `int macos_sapp_depth_format(void)` | 102 |
| `macos_sapp_sample_count` | `int macos_sapp_sample_count(void)` | 106 |
| `macos_sapp_high_dpi` | `bool macos_sapp_high_dpi(void)` | 110 |
| `macos_sapp_dpi_scale` | `float macos_sapp_dpi_scale(void)` | 114 |
| `macos_sapp_run` | `void macos_sapp_run(const sapp_desc* desc)` | 194 |
| ... | (96 total stub functions) | ... |

---

### shims/linux/x11.c — X11 Dynamic Loading Shim
**Lines:** ~450

#### Loader Functions
| Function | Signature | Line |
|----------|-----------|------|
| `load_X11_procs` | `static void load_X11_procs(void)` | 79 |
| `load_Xcursor_procs` | `static void load_Xcursor_procs(void)` | 134 |
| `load_Xi_procs` | `static void load_Xi_procs(void)` | 147 |

#### X11 Wrapper Functions (Selected)
| Function | Signature | Line |
|----------|-----------|------|
| `XOpenDisplay` | `Display* XOpenDisplay(const char* display_name)` | 154 |
| `XCloseDisplay` | `int XCloseDisplay(Display* display)` | 160 |
| `XFlush` | `int XFlush(Display* display)` | 166 |
| `XNextEvent` | `int XNextEvent(Display* display, XEvent* event_return)` | 172 |
| `XPending` | `int XPending(Display* display)` | 178 |
| `XInitThreads` | `Status XInitThreads(void)` | 184 |
| `XFilterEvent` | `Bool XFilterEvent(XEvent* event, Window w)` | 190 |
| `XCreateWindow` | `Window XCreateWindow(Display*, Window, int, int, unsigned int, unsigned int, unsigned int, int, unsigned int, Visual*, unsigned long, XSetWindowAttributes*)` | 270 |
| `XInternAtom` | `Atom XInternAtom(Display* display, const char* atom_name, Bool only_if_exists)` | 310 |
| `XcursorImageLoadCursor` | `Cursor XcursorImageLoadCursor(Display* dpy, const XcursorImage* image)` | 360 |
| `XIQueryVersion` | `Status XIQueryVersion(Display* dpy, int* major_version_inout, int* minor_version_inout)` | 370 |
| `XISelectEvents` | `int XISelectEvents(Display* dpy, Window win, XIEventMask* masks, int num_masks)` | 376 |

---

### shims/linux/gl.c — OpenGL Dynamic Loading Shim
**Lines:** ~6172 (extensive GL function coverage)

#### Loader Function
| Function | Signature | Line |
|----------|-----------|------|
| `load_gl` | `static void load_gl(void)` | ~615 |

#### GL Wrapper Functions (Selected - 400+ total)
| Function | Signature | Line |
|----------|-----------|------|
| `glClear` | `void glClear(GLbitfield mask)` | ~1200 |
| `glClearColor` | `void glClearColor(GLfloat red, GLfloat green, GLfloat blue, GLfloat alpha)` | ~1220 |
| `glViewport` | `void glViewport(GLint x, GLint y, GLsizei width, GLsizei height)` | ~2800 |
| `glBindBuffer` | `void glBindBuffer(GLenum target, GLuint buffer)` | ~1050 |
| `glGenBuffers` | `void glGenBuffers(GLsizei n, GLuint* buffers)` | ~1950 |
| `glCreateShader` | `GLuint glCreateShader(GLenum type)` | ~1700 |
| `glShaderSource` | `void glShaderSource(GLuint shader, GLsizei count, const GLchar** string, const GLint* length)` | ~3200 |
| `glCompileShader` | `void glCompileShader(GLuint shader)` | ~1650 |
| `glCreateProgram` | `GLuint glCreateProgram(void)` | ~1690 |
| `glLinkProgram` | `void glLinkProgram(GLuint program)` | ~2350 |
| `glUseProgram` | `void glUseProgram(GLuint program)` | ~3400 |
| `glDrawArrays` | `void glDrawArrays(GLenum mode, GLint first, GLsizei count)` | ~1780 |
| `glDrawElements` | `void glDrawElements(GLenum mode, GLsizei count, GLenum type, const void* indices)` | ~1800 |

---

### shims/sokol/sokol_windows.c — Windows Backend
**Lines:** ~300 (includes type definitions + includes)

This file primarily includes type definitions and then includes sokol headers with SOKOL_IMPL defined, generating the Windows implementation from upstream.

#### Windows-Specific Type Definitions (Lines 1-280)
- `LARGE_INTEGER` (line 11)
- `RECT` (line 21)
- `POINT` (line 28)
- `MSG` (line 33)
- `PIXELFORMATDESCRIPTOR` (line 71)
- `MONITORINFO` (line 99)
- `RAWINPUTDEVICE` (line 111)
- `WNDCLASSW` (line 188)
- `BITMAPV5HEADER` (line 236)
- `ICONINFO` (line 273)

#### Helper Function
| Function | Signature | Line |
|----------|-----------|------|
| `freopen_s` | `static errno_t freopen_s(FILE** stream, const char* fileName, const char* mode, FILE* oldStream)` | 283 |

---

## NVAPI STRUCTURES (nvapi/nvapi_decl.h)

| Structure | Purpose | Line |
|-----------|---------|------|
| `NvDRSSessionHandle` | DRS Session handle | 9 |
| `NvDRSProfileHandle` | DRS Profile handle | 10 |
| `NvAPI_UnicodeString` | Unicode string type | 13 |
| `NvAPI_ShortString` | Short ASCII string | 14 |
| `NVDRS_SETTING_TYPE` | Setting type enum | 18 |
| `NVDRS_SETTING_LOCATION` | Setting location enum | 26 |
| `NVDRS_GPU_SUPPORT` | GPU support flags | 34 |
| `NVDRS_BINARY_SETTING` | Binary setting data | 67 |
| `NVDRS_SETTING_VALUES` | Setting value container | 73 |
| `NVDRS_SETTING_V1` | Setting structure v1 | 93 |
| `NVDRS_APPLICATION_V4` | Application structure v4 | 121 |
| `NVDRS_PROFILE_V1` | Profile structure v1 | 139 |

---

## KEY UPSTREAM SOKOL HEADERS (deps/sokol/)

### sokol_app.h — Application Framework
**Lines:** ~12,300  
**Key APIs:** Window creation, input events, platform abstraction

### sokol_gfx.h — Graphics
**Lines:** ~19,900  
**Key APIs:** GPU resource management, render passes, draw calls

### sokol_log.h — Logging
**Key Function:**
| Function | Signature |
|----------|-----------|
| `slog_func` | `void slog_func(const char* tag, uint32_t log_level, uint32_t log_item, const char* message, uint32_t line_nr, const char* filename, void* user_data)` |

### sokol_glue.h — sokol_app + sokol_gfx Glue
**Key Functions:**
| Function | Signature |
|----------|-----------|
| `sglue_environment` | `sg_environment sglue_environment(void)` |
| `sglue_swapchain` | `sg_swapchain sglue_swapchain(void)` |

---

## BUILD SYSTEM

### build (shell script)
| Section | Description | Line |
|---------|-------------|------|
| Compiler detection | Check cosmocc in PATH | 3-7 |
| FLAGS definition | Common compiler flags | 11-16 |
| Platform flags | Per-platform include paths | 18-24 |
| Compilation commands | Generate parallel build | 31-50 |
| Linking | Final binary generation | 60 |

---

## GENERATOR SCRIPTS (Build-time only, NOT compiled)

### shims/sokol/gen-sokol (Python)
**Note:** Used at development time to generate C shims. NOT part of runtime.

| Function | Purpose | Line |
|----------|---------|------|
| `main` | Generate all platform files | 223 |
| `make_platform_name` | Create prefixed function name | 260 |
| `parse_c_signature` | Parse C function signature | 264 |
| `arg_list` | Generate argument list string | 297 |
| `forward_list` | Generate forwarding args | 306 |

---

## FILE INVENTORY

### Source Files (.c)
| File | Lines | Functions |
|------|-------|-----------|
| `main.c` | 109 | 5 |
| `win32_tweaks.c` | 15 | 1 |
| `nvapi/nvapi.c` | 105 | 1 |
| `shims/sokol/sokol_cosmo.c` | ~3100 | 190 |
| `shims/sokol/sokol_linux.c` | 15 | 0 (includes) |
| `shims/sokol/sokol_windows.c` | 295 | 1 |
| `shims/sokol/sokol_macos.c` | 750 | ~97 |
| `shims/sokol/sokol_shared.c` | 9 | 0 (includes) |
| `shims/linux/gl.c` | 6172 | ~400 |
| `shims/linux/x11.c` | 450 | ~50 |

### Header Files (.h)
| File | Purpose |
|------|---------|
| `win32_tweaks.h` | Console helper decl |
| `nvapi/nvapi.h` | NVIDIA API decl |
| `nvapi/nvapi_decl.h` | NVIDIA types/structs |
| `shims/sokol/sokol_linux.h` | Linux function prefixes |
| `shims/sokol/sokol_windows.h` | Windows function prefixes |
| `shims/sokol/sokol_macos.h` | macOS function prefixes |
| `shims/win32/shellapi.h` | Windows shell API shim |
| `shims/win32/windowsx.h` | Windows extended macros |

---

## SUMMARY STATISTICS

| Metric | Count |
|--------|-------|
| **Total Source Files** | 10 |
| **Total Header Files** | 8 |
| **Project Functions** | ~7 |
| **Sokol Dispatch Functions** | 190 |
| **GL Wrapper Functions** | ~400 |
| **X11 Wrapper Functions** | ~50 |
| **macOS Stub Functions** | ~97 |
| **Total Functions (Project)** | ~750 |

---

## UPSTREAM TRACKING

### Dependencies
| Dependency | Source | Current |
|------------|--------|---------|
| sokol | github.com/floooh/sokol | Submodule in deps/sokol |
| cimgui | github.com/cimgui/cimgui | Submodule in deps/cimgui |
| cosmopolitan | github.com/jart/cosmopolitan | Requires v3.9.5+ |

### Sync Points
- `deps/sokol/` - Upstream floooh/sokol
- `deps/cimgui/` - Upstream cimgui/cimgui  
- Build system compatibility with cosmocc

---

*End of Source Manifest*
