# cosmo-sokol Source Manifest — AMD64/AArch64 Assembly & ABI Analysis

**Specialist:** asm (AMD64/AArch64 assembly, ABI, calling conventions)  
**Repository:** ludoplex/cosmo-sokol  
**Path:** `C:\cosmo-sokol`  
**Generated:** 2026-02-09T19:14:00-07:00  
**Round:** 1

---

## Executive Summary

The cosmo-sokol fork is a **Cosmopolitan Libc** port of the sokol graphics libraries. From an ABI/assembly perspective:

### Key ABI Architecture Findings

1. **NO INLINE ASSEMBLY** — The codebase contains zero inline assembly (no `__asm__`, no `asm()` blocks)
2. **Runtime Platform Dispatch** — Uses Cosmopolitan's `IsLinux()`, `IsWindows()`, `IsXnu()` for runtime ABI switching
3. **Dynamic Library Trampolines** — Critical use of `cosmo_dltramp()` for cross-ABI function pointer calls
4. **Win32 Calling Convention** — Proper `WINAPI` attribute usage for Windows API callbacks
5. **No Architecture-Specific Code** — All platform differences handled via conditional compilation, not architecture

### ABI-Critical Components

| Component | ABI Concern | Status |
|-----------|-------------|--------|
| `cosmo_dltramp()` | Cross-ABI function trampolines | Linux X11/GL shims |
| `WNDPROC` callbacks | Win32 calling convention | Windows shims |
| `NVAPI` | Win64 calling convention | nvapi.c |
| Struct return types | ABI-sensitive (sret) | sokol_gfx structs |

---

## Source Manifest — Function Index

### File: `main.c`
**Path:** `C:\cosmo-sokol\main.c`

| Function | Signature | Line |
|----------|-----------|------|
| `init` | `void init(void)` | 27 |
| `frame` | `void frame(void)` | 47 |
| `cleanup` | `void cleanup(void)` | 91 |
| `input` | `void input(const sapp_event* event)` | 96 |
| `main` | `int main(int argc, char* argv[])` | 100 |

---

### File: `win32_tweaks.c`
**Path:** `C:\cosmo-sokol\win32_tweaks.c`

| Function | Signature | Line |
|----------|-----------|------|
| `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` | 5 |

---

### File: `nvapi/nvapi.c`
**Path:** `C:\cosmo-sokol\nvapi\nvapi.c`

| Function | Signature | Line |
|----------|-----------|------|
| `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` | 39 |

**ABI Notes:** Uses Windows x64 calling convention via `WINAPI` typedef. Loads `nvapi64.dll` dynamically.

---

### File: `shims/sokol/sokol_cosmo.c` — Runtime Dispatch Layer
**Path:** `C:\cosmo-sokol\shims\sokol\sokol_cosmo.c`

This file provides the **unified public API** that dispatches to platform-specific implementations at runtime.

#### sapp_* Functions (sokol_app)

| Function | Signature | Line |
|----------|-----------|------|
| `sapp_isvalid` | `bool sapp_isvalid(void)` | 12 |
| `sapp_width` | `int sapp_width(void)` | 24 |
| `sapp_widthf` | `float sapp_widthf(void)` | 36 |
| `sapp_height` | `int sapp_height(void)` | 48 |
| `sapp_heightf` | `float sapp_heightf(void)` | 60 |
| `sapp_color_format` | `int sapp_color_format(void)` | 72 |
| `sapp_depth_format` | `int sapp_depth_format(void)` | 84 |
| `sapp_sample_count` | `int sapp_sample_count(void)` | 96 |
| `sapp_high_dpi` | `bool sapp_high_dpi(void)` | 108 |
| `sapp_dpi_scale` | `float sapp_dpi_scale(void)` | 120 |
| `sapp_show_keyboard` | `void sapp_show_keyboard(bool show)` | 132 |
| `sapp_keyboard_shown` | `bool sapp_keyboard_shown(void)` | 146 |
| `sapp_is_fullscreen` | `bool sapp_is_fullscreen(void)` | 158 |
| `sapp_toggle_fullscreen` | `void sapp_toggle_fullscreen(void)` | 170 |
| `sapp_show_mouse` | `void sapp_show_mouse(bool show)` | 184 |
| `sapp_mouse_shown` | `bool sapp_mouse_shown(void)` | 198 |
| `sapp_lock_mouse` | `void sapp_lock_mouse(bool lock)` | 210 |
| `sapp_mouse_locked` | `bool sapp_mouse_locked(void)` | 224 |
| `sapp_set_mouse_cursor` | `void sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 236 |
| `sapp_get_mouse_cursor` | `sapp_mouse_cursor sapp_get_mouse_cursor(void)` | 250 |
| `sapp_userdata` | `void* sapp_userdata(void)` | 262 |
| `sapp_query_desc` | `sapp_desc sapp_query_desc(void)` | 274 |
| `sapp_request_quit` | `void sapp_request_quit(void)` | 286 |
| `sapp_cancel_quit` | `void sapp_cancel_quit(void)` | 300 |
| `sapp_quit` | `void sapp_quit(void)` | 314 |
| `sapp_consume_event` | `void sapp_consume_event(void)` | 328 |
| `sapp_frame_count` | `uint64_t sapp_frame_count(void)` | 342 |
| `sapp_frame_duration` | `double sapp_frame_duration(void)` | 354 |
| `sapp_set_clipboard_string` | `void sapp_set_clipboard_string(const char* str)` | 366 |
| `sapp_get_clipboard_string` | `const char* sapp_get_clipboard_string(void)` | 380 |
| `sapp_set_window_title` | `void sapp_set_window_title(const char* str)` | 392 |
| `sapp_set_icon` | `void sapp_set_icon(const sapp_icon_desc* icon_desc)` | 406 |
| `sapp_get_num_dropped_files` | `int sapp_get_num_dropped_files(void)` | 420 |
| `sapp_get_dropped_file_path` | `const char* sapp_get_dropped_file_path(int index)` | 432 |
| `sapp_run` | `void sapp_run(const sapp_desc* desc)` | 444 |
| `sapp_egl_get_display` | `const void* sapp_egl_get_display(void)` | 458 |
| `sapp_egl_get_context` | `const void* sapp_egl_get_context(void)` | 470 |
| `sapp_html5_ask_leave_site` | `void sapp_html5_ask_leave_site(bool ask)` | 482 |
| `sapp_html5_get_dropped_file_size` | `uint32_t sapp_html5_get_dropped_file_size(int index)` | 496 |
| `sapp_html5_fetch_dropped_file` | `void sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 508 |
| `sapp_metal_get_device` | `const void* sapp_metal_get_device(void)` | 522 |
| `sapp_metal_get_current_drawable` | `const void* sapp_metal_get_current_drawable(void)` | 534 |
| `sapp_metal_get_depth_stencil_texture` | `const void* sapp_metal_get_depth_stencil_texture(void)` | 546 |
| `sapp_metal_get_msaa_color_texture` | `const void* sapp_metal_get_msaa_color_texture(void)` | 558 |
| `sapp_macos_get_window` | `const void* sapp_macos_get_window(void)` | 570 |
| `sapp_ios_get_window` | `const void* sapp_ios_get_window(void)` | 582 |
| `sapp_d3d11_get_device` | `const void* sapp_d3d11_get_device(void)` | 594 |
| `sapp_d3d11_get_device_context` | `const void* sapp_d3d11_get_device_context(void)` | 606 |
| `sapp_d3d11_get_swap_chain` | `const void* sapp_d3d11_get_swap_chain(void)` | 618 |
| `sapp_d3d11_get_render_view` | `const void* sapp_d3d11_get_render_view(void)` | 630 |
| `sapp_d3d11_get_resolve_view` | `const void* sapp_d3d11_get_resolve_view(void)` | 642 |
| `sapp_d3d11_get_depth_stencil_view` | `const void* sapp_d3d11_get_depth_stencil_view(void)` | 654 |
| `sapp_win32_get_hwnd` | `const void* sapp_win32_get_hwnd(void)` | 666 |
| `sapp_wgpu_get_device` | `const void* sapp_wgpu_get_device(void)` | 678 |
| `sapp_wgpu_get_render_view` | `const void* sapp_wgpu_get_render_view(void)` | 690 |
| `sapp_wgpu_get_resolve_view` | `const void* sapp_wgpu_get_resolve_view(void)` | 702 |
| `sapp_wgpu_get_depth_stencil_view` | `const void* sapp_wgpu_get_depth_stencil_view(void)` | 714 |
| `sapp_gl_get_framebuffer` | `uint32_t sapp_gl_get_framebuffer(void)` | 726 |
| `sapp_gl_get_major_version` | `int sapp_gl_get_major_version(void)` | 738 |
| `sapp_gl_get_minor_version` | `int sapp_gl_get_minor_version(void)` | 750 |
| `sapp_android_get_native_activity` | `const void* sapp_android_get_native_activity(void)` | 762 |

#### sg_* Functions (sokol_gfx)

| Function | Signature | Line |
|----------|-----------|------|
| `sg_setup` | `void sg_setup(const sg_desc* desc)` | 774 |
| `sg_shutdown` | `void sg_shutdown(void)` | 788 |
| `sg_isvalid` | `bool sg_isvalid(void)` | 802 |
| `sg_reset_state_cache` | `void sg_reset_state_cache(void)` | 814 |
| `sg_install_trace_hooks` | `sg_trace_hooks sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` | 828 |
| `sg_push_debug_group` | `void sg_push_debug_group(const char* name)` | 840 |
| `sg_pop_debug_group` | `void sg_pop_debug_group(void)` | 854 |
| `sg_add_commit_listener` | `bool sg_add_commit_listener(sg_commit_listener listener)` | 866 |
| `sg_remove_commit_listener` | `bool sg_remove_commit_listener(sg_commit_listener listener)` | 878 |
| `sg_make_buffer` | `sg_buffer sg_make_buffer(const sg_buffer_desc* desc)` | 890 |
| `sg_make_image` | `sg_image sg_make_image(const sg_image_desc* desc)` | 902 |
| `sg_make_sampler` | `sg_sampler sg_make_sampler(const sg_sampler_desc* desc)` | 914 |
| `sg_make_shader` | `sg_shader sg_make_shader(const sg_shader_desc* desc)` | 926 |
| `sg_make_pipeline` | `sg_pipeline sg_make_pipeline(const sg_pipeline_desc* desc)` | 938 |
| `sg_make_attachments` | `sg_attachments sg_make_attachments(const sg_attachments_desc* desc)` | 950 |
| `sg_destroy_buffer` | `void sg_destroy_buffer(sg_buffer buf)` | 962 |
| `sg_destroy_image` | `void sg_destroy_image(sg_image img)` | 976 |
| `sg_destroy_sampler` | `void sg_destroy_sampler(sg_sampler smp)` | 990 |
| `sg_destroy_shader` | `void sg_destroy_shader(sg_shader shd)` | 1004 |
| `sg_destroy_pipeline` | `void sg_destroy_pipeline(sg_pipeline pip)` | 1018 |
| `sg_destroy_attachments` | `void sg_destroy_attachments(sg_attachments atts)` | 1032 |
| `sg_update_buffer` | `void sg_update_buffer(sg_buffer buf, const sg_range* data)` | 1046 |
| `sg_update_image` | `void sg_update_image(sg_image img, const sg_image_data* data)` | 1060 |
| `sg_append_buffer` | `int sg_append_buffer(sg_buffer buf, const sg_range* data)` | 1074 |
| `sg_query_buffer_overflow` | `bool sg_query_buffer_overflow(sg_buffer buf)` | 1086 |
| `sg_query_buffer_will_overflow` | `bool sg_query_buffer_will_overflow(sg_buffer buf, size_t size)` | 1098 |
| `sg_begin_pass` | `void sg_begin_pass(const sg_pass* pass)` | 1110 |
| `sg_apply_viewport` | `void sg_apply_viewport(int x, int y, int width, int height, bool origin_top_left)` | 1124 |
| `sg_apply_viewportf` | `void sg_apply_viewportf(float x, float y, float width, float height, bool origin_top_left)` | 1138 |
| `sg_apply_scissor_rect` | `void sg_apply_scissor_rect(int x, int y, int width, int height, bool origin_top_left)` | 1152 |
| `sg_apply_scissor_rectf` | `void sg_apply_scissor_rectf(float x, float y, float width, float height, bool origin_top_left)` | 1166 |
| `sg_apply_pipeline` | `void sg_apply_pipeline(sg_pipeline pip)` | 1180 |
| `sg_apply_bindings` | `void sg_apply_bindings(const sg_bindings* bindings)` | 1194 |
| `sg_apply_uniforms` | `void sg_apply_uniforms(int ub_slot, const sg_range* data)` | 1208 |
| `sg_draw` | `void sg_draw(int base_element, int num_elements, int num_instances)` | 1222 |
| `sg_end_pass` | `void sg_end_pass(void)` | 1236 |
| `sg_commit` | `void sg_commit(void)` | 1250 |
| `sg_query_desc` | `sg_desc sg_query_desc(void)` | 1264 |
| `sg_query_backend` | `sg_backend sg_query_backend(void)` | 1276 |
| `sg_query_features` | `sg_features sg_query_features(void)` | 1288 |
| `sg_query_limits` | `sg_limits sg_query_limits(void)` | 1300 |
| `sg_query_pixelformat` | `sg_pixelformat_info sg_query_pixelformat(sg_pixel_format fmt)` | 1312 |
| `sg_query_row_pitch` | `int sg_query_row_pitch(sg_pixel_format fmt, int width, int row_align_bytes)` | 1324 |
| `sg_query_surface_pitch` | `int sg_query_surface_pitch(sg_pixel_format fmt, int width, int height, int row_align_bytes)` | 1336 |
| `sg_query_buffer_state` | `sg_resource_state sg_query_buffer_state(sg_buffer buf)` | 1348 |
| `sg_query_image_state` | `sg_resource_state sg_query_image_state(sg_image img)` | 1360 |
| `sg_query_sampler_state` | `sg_resource_state sg_query_sampler_state(sg_sampler smp)` | 1372 |
| `sg_query_shader_state` | `sg_resource_state sg_query_shader_state(sg_shader shd)` | 1384 |
| `sg_query_pipeline_state` | `sg_resource_state sg_query_pipeline_state(sg_pipeline pip)` | 1396 |
| `sg_query_attachments_state` | `sg_resource_state sg_query_attachments_state(sg_attachments atts)` | 1408 |
| `sg_query_buffer_info` | `sg_buffer_info sg_query_buffer_info(sg_buffer buf)` | 1420 |
| `sg_query_image_info` | `sg_image_info sg_query_image_info(sg_image img)` | 1432 |
| `sg_query_sampler_info` | `sg_sampler_info sg_query_sampler_info(sg_sampler smp)` | 1444 |
| `sg_query_shader_info` | `sg_shader_info sg_query_shader_info(sg_shader shd)` | 1456 |
| `sg_query_pipeline_info` | `sg_pipeline_info sg_query_pipeline_info(sg_pipeline pip)` | 1468 |
| `sg_query_attachments_info` | `sg_attachments_info sg_query_attachments_info(sg_attachments atts)` | 1480 |
| `sg_query_buffer_desc` | `sg_buffer_desc sg_query_buffer_desc(sg_buffer buf)` | 1492 |
| `sg_query_image_desc` | `sg_image_desc sg_query_image_desc(sg_image img)` | 1504 |
| `sg_query_sampler_desc` | `sg_sampler_desc sg_query_sampler_desc(sg_sampler smp)` | 1516 |
| `sg_query_shader_desc` | `sg_shader_desc sg_query_shader_desc(sg_shader shd)` | 1528 |
| `sg_query_pipeline_desc` | `sg_pipeline_desc sg_query_pipeline_desc(sg_pipeline pip)` | 1540 |
| `sg_query_attachments_desc` | `sg_attachments_desc sg_query_attachments_desc(sg_attachments atts)` | 1552 |
| `sg_query_buffer_defaults` | `sg_buffer_desc sg_query_buffer_defaults(const sg_buffer_desc* desc)` | 1564 |
| `sg_query_image_defaults` | `sg_image_desc sg_query_image_defaults(const sg_image_desc* desc)` | 1576 |
| `sg_query_sampler_defaults` | `sg_sampler_desc sg_query_sampler_defaults(const sg_sampler_desc* desc)` | 1588 |
| `sg_query_shader_defaults` | `sg_shader_desc sg_query_shader_defaults(const sg_shader_desc* desc)` | 1600 |
| `sg_query_pipeline_defaults` | `sg_pipeline_desc sg_query_pipeline_defaults(const sg_pipeline_desc* desc)` | 1612 |
| `sg_query_attachments_defaults` | `sg_attachments_desc sg_query_attachments_defaults(const sg_attachments_desc* desc)` | 1624 |
| `sg_alloc_buffer` | `sg_buffer sg_alloc_buffer(void)` | 1636 |
| `sg_alloc_image` | `sg_image sg_alloc_image(void)` | 1648 |
| `sg_alloc_sampler` | `sg_sampler sg_alloc_sampler(void)` | 1660 |
| `sg_alloc_shader` | `sg_shader sg_alloc_shader(void)` | 1672 |
| `sg_alloc_pipeline` | `sg_pipeline sg_alloc_pipeline(void)` | 1684 |
| `sg_alloc_attachments` | `sg_attachments sg_alloc_attachments(void)` | 1696 |
| `sg_dealloc_buffer` | `void sg_dealloc_buffer(sg_buffer buf)` | 1708 |
| `sg_dealloc_image` | `void sg_dealloc_image(sg_image img)` | 1722 |
| `sg_dealloc_sampler` | `void sg_dealloc_sampler(sg_sampler smp)` | 1736 |
| `sg_dealloc_shader` | `void sg_dealloc_shader(sg_shader shd)` | 1750 |
| `sg_dealloc_pipeline` | `void sg_dealloc_pipeline(sg_pipeline pip)` | 1764 |
| `sg_dealloc_attachments` | `void sg_dealloc_attachments(sg_attachments attachments)` | 1778 |
| `sg_init_buffer` | `void sg_init_buffer(sg_buffer buf, const sg_buffer_desc* desc)` | 1792 |
| `sg_init_image` | `void sg_init_image(sg_image img, const sg_image_desc* desc)` | 1806 |
| `sg_init_sampler` | `void sg_init_sampler(sg_sampler smg, const sg_sampler_desc* desc)` | 1820 |
| `sg_init_shader` | `void sg_init_shader(sg_shader shd, const sg_shader_desc* desc)` | 1834 |
| `sg_init_pipeline` | `void sg_init_pipeline(sg_pipeline pip, const sg_pipeline_desc* desc)` | 1848 |
| `sg_init_attachments` | `void sg_init_attachments(sg_attachments attachments, const sg_attachments_desc* desc)` | 1862 |
| `sg_uninit_buffer` | `void sg_uninit_buffer(sg_buffer buf)` | 1876 |
| `sg_uninit_image` | `void sg_uninit_image(sg_image img)` | 1890 |
| `sg_uninit_sampler` | `void sg_uninit_sampler(sg_sampler smp)` | 1904 |
| `sg_uninit_shader` | `void sg_uninit_shader(sg_shader shd)` | 1918 |
| `sg_uninit_pipeline` | `void sg_uninit_pipeline(sg_pipeline pip)` | 1932 |
| `sg_uninit_attachments` | `void sg_uninit_attachments(sg_attachments atts)` | 1946 |
| `sg_fail_buffer` | `void sg_fail_buffer(sg_buffer buf)` | 1960 |
| `sg_fail_image` | `void sg_fail_image(sg_image img)` | 1974 |
| `sg_fail_sampler` | `void sg_fail_sampler(sg_sampler smp)` | 1988 |
| `sg_fail_shader` | `void sg_fail_shader(sg_shader shd)` | 2002 |
| `sg_fail_pipeline` | `void sg_fail_pipeline(sg_pipeline pip)` | 2016 |
| `sg_fail_attachments` | `void sg_fail_attachments(sg_attachments atts)` | 2030 |
| `sg_enable_frame_stats` | `void sg_enable_frame_stats(void)` | 2044 |
| `sg_disable_frame_stats` | `void sg_disable_frame_stats(void)` | 2058 |
| `sg_frame_stats_enabled` | `bool sg_frame_stats_enabled(void)` | 2070 |
| `sg_query_frame_stats` | `sg_frame_stats sg_query_frame_stats(void)` | 2082 |
| `sg_d3d11_device` | `const void* sg_d3d11_device(void)` | 2094 |
| `sg_d3d11_device_context` | `const void* sg_d3d11_device_context(void)` | 2106 |
| `sg_d3d11_query_buffer_info` | `sg_d3d11_buffer_info sg_d3d11_query_buffer_info(sg_buffer buf)` | 2118 |
| `sg_d3d11_query_image_info` | `sg_d3d11_image_info sg_d3d11_query_image_info(sg_image img)` | 2130 |
| `sg_d3d11_query_sampler_info` | `sg_d3d11_sampler_info sg_d3d11_query_sampler_info(sg_sampler smp)` | 2142 |
| `sg_d3d11_query_shader_info` | `sg_d3d11_shader_info sg_d3d11_query_shader_info(sg_shader shd)` | 2154 |
| `sg_d3d11_query_pipeline_info` | `sg_d3d11_pipeline_info sg_d3d11_query_pipeline_info(sg_pipeline pip)` | 2166 |
| `sg_d3d11_query_attachments_info` | `sg_d3d11_attachments_info sg_d3d11_query_attachments_info(sg_attachments atts)` | 2178 |
| `sg_mtl_device` | `const void* sg_mtl_device(void)` | 2190 |
| `sg_mtl_render_command_encoder` | `const void* sg_mtl_render_command_encoder(void)` | 2202 |
| `sg_mtl_query_buffer_info` | `sg_mtl_buffer_info sg_mtl_query_buffer_info(sg_buffer buf)` | 2214 |
| `sg_mtl_query_image_info` | `sg_mtl_image_info sg_mtl_query_image_info(sg_image img)` | 2226 |
| `sg_mtl_query_sampler_info` | `sg_mtl_sampler_info sg_mtl_query_sampler_info(sg_sampler smp)` | 2238 |
| `sg_mtl_query_shader_info` | `sg_mtl_shader_info sg_mtl_query_shader_info(sg_shader shd)` | 2250 |
| `sg_mtl_query_pipeline_info` | `sg_mtl_pipeline_info sg_mtl_query_pipeline_info(sg_pipeline pip)` | 2262 |
| `sg_wgpu_device` | `const void* sg_wgpu_device(void)` | 2274 |
| `sg_wgpu_queue` | `const void* sg_wgpu_queue(void)` | 2286 |
| `sg_wgpu_command_encoder` | `const void* sg_wgpu_command_encoder(void)` | 2298 |
| `sg_wgpu_render_pass_encoder` | `const void* sg_wgpu_render_pass_encoder(void)` | 2310 |
| `sg_wgpu_query_buffer_info` | `sg_wgpu_buffer_info sg_wgpu_query_buffer_info(sg_buffer buf)` | 2322 |
| `sg_wgpu_query_image_info` | `sg_wgpu_image_info sg_wgpu_query_image_info(sg_image img)` | 2334 |
| `sg_wgpu_query_sampler_info` | `sg_wgpu_sampler_info sg_wgpu_query_sampler_info(sg_sampler smp)` | 2346 |
| `sg_wgpu_query_shader_info` | `sg_wgpu_shader_info sg_wgpu_query_shader_info(sg_shader shd)` | 2358 |
| `sg_wgpu_query_pipeline_info` | `sg_wgpu_pipeline_info sg_wgpu_query_pipeline_info(sg_pipeline pip)` | 2370 |
| `sg_wgpu_query_attachments_info` | `sg_wgpu_attachments_info sg_wgpu_query_attachments_info(sg_attachments atts)` | 2382 |
| `sg_gl_query_buffer_info` | `sg_gl_buffer_info sg_gl_query_buffer_info(sg_buffer buf)` | 2394 |
| `sg_gl_query_image_info` | `sg_gl_image_info sg_gl_query_image_info(sg_image img)` | 2406 |
| `sg_gl_query_sampler_info` | `sg_gl_sampler_info sg_gl_query_sampler_info(sg_sampler smp)` | 2418 |
| `sg_gl_query_shader_info` | `sg_gl_shader_info sg_gl_query_shader_info(sg_shader shd)` | 2430 |
| `sg_gl_query_attachments_info` | `sg_gl_attachments_info sg_gl_query_attachments_info(sg_attachments atts)` | 2442 |

---

### File: `shims/sokol/sokol_macos.c` — macOS Stub Implementation
**Path:** `C:\cosmo-sokol\shims\sokol\sokol_macos.c`

**ABI Status:** STUB — macOS requires Objective-C which cosmocc cannot compile.

| Function | Signature | Line |
|----------|-----------|------|
| `_macos_not_implemented` | `static void _macos_not_implemented(const char* func)` | 67 |
| `macos_sapp_isvalid` | `bool macos_sapp_isvalid(void)` | 85 |
| `macos_sapp_width` | `int macos_sapp_width(void)` | 89 |
| `macos_sapp_widthf` | `float macos_sapp_widthf(void)` | 93 |
| `macos_sapp_height` | `int macos_sapp_height(void)` | 97 |
| `macos_sapp_heightf` | `float macos_sapp_heightf(void)` | 101 |
| `macos_sapp_color_format` | `int macos_sapp_color_format(void)` | 105 |
| `macos_sapp_depth_format` | `int macos_sapp_depth_format(void)` | 109 |
| `macos_sapp_sample_count` | `int macos_sapp_sample_count(void)` | 113 |
| `macos_sapp_high_dpi` | `bool macos_sapp_high_dpi(void)` | 117 |
| `macos_sapp_dpi_scale` | `float macos_sapp_dpi_scale(void)` | 121 |
| `macos_sapp_show_keyboard` | `void macos_sapp_show_keyboard(bool show)` | 125 |
| `macos_sapp_keyboard_shown` | `bool macos_sapp_keyboard_shown(void)` | 129 |
| `macos_sapp_is_fullscreen` | `bool macos_sapp_is_fullscreen(void)` | 133 |
| `macos_sapp_toggle_fullscreen` | `void macos_sapp_toggle_fullscreen(void)` | 137 |
| `macos_sapp_show_mouse` | `void macos_sapp_show_mouse(bool show)` | 140 |
| `macos_sapp_mouse_shown` | `bool macos_sapp_mouse_shown(void)` | 144 |
| `macos_sapp_lock_mouse` | `void macos_sapp_lock_mouse(bool lock)` | 148 |
| `macos_sapp_mouse_locked` | `bool macos_sapp_mouse_locked(void)` | 152 |
| `macos_sapp_set_mouse_cursor` | `void macos_sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 156 |
| `macos_sapp_get_mouse_cursor` | `sapp_mouse_cursor macos_sapp_get_mouse_cursor(void)` | 160 |
| `macos_sapp_userdata` | `void* macos_sapp_userdata(void)` | 164 |
| `macos_sapp_query_desc` | `sapp_desc macos_sapp_query_desc(void)` | 168 |
| `macos_sapp_request_quit` | `void macos_sapp_request_quit(void)` | 172 |
| `macos_sapp_cancel_quit` | `void macos_sapp_cancel_quit(void)` | 175 |
| `macos_sapp_quit` | `void macos_sapp_quit(void)` | 178 |
| `macos_sapp_consume_event` | `void macos_sapp_consume_event(void)` | 185 |
| `macos_sapp_frame_count` | `uint64_t macos_sapp_frame_count(void)` | 188 |
| `macos_sapp_frame_duration` | `double macos_sapp_frame_duration(void)` | 192 |
| `macos_sapp_set_clipboard_string` | `void macos_sapp_set_clipboard_string(const char* str)` | 202 |
| `macos_sapp_get_clipboard_string` | `const char* macos_sapp_get_clipboard_string(void)` | 206 |
| `macos_sapp_set_window_title` | `void macos_sapp_set_window_title(const char* str)` | 210 |
| `macos_sapp_set_icon` | `void macos_sapp_set_icon(const sapp_icon_desc* icon_desc)` | 214 |
| `macos_sapp_get_num_dropped_files` | `int macos_sapp_get_num_dropped_files(void)` | 218 |
| `macos_sapp_get_dropped_file_path` | `const char* macos_sapp_get_dropped_file_path(int index)` | 222 |
| `macos_sapp_run` | `void macos_sapp_run(const sapp_desc* desc)` | 227 |
| `macos_sapp_egl_get_display` | `const void* macos_sapp_egl_get_display(void)` | 251 |
| `macos_sapp_egl_get_context` | `const void* macos_sapp_egl_get_context(void)` | 255 |
| `macos_sapp_html5_ask_leave_site` | `void macos_sapp_html5_ask_leave_site(bool ask)` | 259 |
| `macos_sapp_html5_get_dropped_file_size` | `uint32_t macos_sapp_html5_get_dropped_file_size(int index)` | 263 |
| `macos_sapp_html5_fetch_dropped_file` | `void macos_sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 268 |
| `macos_sapp_metal_get_device` | `const void* macos_sapp_metal_get_device(void)` | 272 |
| `macos_sapp_metal_get_current_drawable` | `const void* macos_sapp_metal_get_current_drawable(void)` | 276 |
| `macos_sapp_metal_get_depth_stencil_texture` | `const void* macos_sapp_metal_get_depth_stencil_texture(void)` | 280 |
| `macos_sapp_metal_get_msaa_color_texture` | `const void* macos_sapp_metal_get_msaa_color_texture(void)` | 284 |
| `macos_sapp_macos_get_window` | `const void* macos_sapp_macos_get_window(void)` | 288 |
| `macos_sapp_ios_get_window` | `const void* macos_sapp_ios_get_window(void)` | 292 |
| `macos_sapp_d3d11_get_device` | `const void* macos_sapp_d3d11_get_device(void)` | 296 |
| `macos_sapp_d3d11_get_device_context` | `const void* macos_sapp_d3d11_get_device_context(void)` | 300 |
| `macos_sapp_d3d11_get_swap_chain` | `const void* macos_sapp_d3d11_get_swap_chain(void)` | 304 |
| `macos_sapp_d3d11_get_render_view` | `const void* macos_sapp_d3d11_get_render_view(void)` | 308 |
| `macos_sapp_d3d11_get_resolve_view` | `const void* macos_sapp_d3d11_get_resolve_view(void)` | 312 |
| `macos_sapp_d3d11_get_depth_stencil_view` | `const void* macos_sapp_d3d11_get_depth_stencil_view(void)` | 316 |
| `macos_sapp_win32_get_hwnd` | `const void* macos_sapp_win32_get_hwnd(void)` | 320 |
| `macos_sapp_wgpu_get_device` | `const void* macos_sapp_wgpu_get_device(void)` | 324 |
| `macos_sapp_wgpu_get_render_view` | `const void* macos_sapp_wgpu_get_render_view(void)` | 328 |
| `macos_sapp_wgpu_get_resolve_view` | `const void* macos_sapp_wgpu_get_resolve_view(void)` | 332 |
| `macos_sapp_wgpu_get_depth_stencil_view` | `const void* macos_sapp_wgpu_get_depth_stencil_view(void)` | 336 |
| `macos_sapp_gl_get_framebuffer` | `uint32_t macos_sapp_gl_get_framebuffer(void)` | 340 |
| `macos_sapp_gl_get_major_version` | `int macos_sapp_gl_get_major_version(void)` | 344 |
| `macos_sapp_gl_get_minor_version` | `int macos_sapp_gl_get_minor_version(void)` | 348 |
| `macos_sapp_android_get_native_activity` | `const void* macos_sapp_android_get_native_activity(void)` | 352 |
| `macos_sg_setup` | `void macos_sg_setup(const sg_desc* desc)` | 362 |
| `macos_sg_shutdown` | `void macos_sg_shutdown(void)` | 369 |
| `macos_sg_isvalid` | `bool macos_sg_isvalid(void)` | 373 |
| `macos_sg_reset_state_cache` | `void macos_sg_reset_state_cache(void)` | 377 |
| `macos_sg_install_trace_hooks` | `sg_trace_hooks macos_sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` | 380 |
| `macos_sg_push_debug_group` | `void macos_sg_push_debug_group(const char* name)` | 386 |
| `macos_sg_pop_debug_group` | `void macos_sg_pop_debug_group(void)` | 390 |
| `macos_sg_add_commit_listener` | `bool macos_sg_add_commit_listener(sg_commit_listener listener)` | 393 |
| `macos_sg_remove_commit_listener` | `bool macos_sg_remove_commit_listener(sg_commit_listener listener)` | 398 |
| `macos_sg_make_buffer` | `sg_buffer macos_sg_make_buffer(const sg_buffer_desc* desc)` | 403 |
| `macos_sg_make_image` | `sg_image macos_sg_make_image(const sg_image_desc* desc)` | 409 |
| `macos_sg_make_sampler` | `sg_sampler macos_sg_make_sampler(const sg_sampler_desc* desc)` | 415 |
| `macos_sg_make_shader` | `sg_shader macos_sg_make_shader(const sg_shader_desc* desc)` | 421 |
| `macos_sg_make_pipeline` | `sg_pipeline macos_sg_make_pipeline(const sg_pipeline_desc* desc)` | 427 |
| `macos_sg_make_attachments` | `sg_attachments macos_sg_make_attachments(const sg_attachments_desc* desc)` | 433 |

*(Additional macos_sg_* stubs continue in file)*

---

### File: `shims/linux/x11.c` — X11 Dynamic Loading Shim
**Path:** `C:\cosmo-sokol\shims\linux\x11.c`

**ABI-CRITICAL:** Uses `cosmo_dltramp()` for cross-ABI function trampolines.

| Function | Signature | Line |
|----------|-----------|------|
| `load_X11_procs` | `static void load_X11_procs(void)` | 93 |
| `load_Xcursor_procs` | `static void load_Xcursor_procs(void)` | 189 |
| `load_Xi_procs` | `static void load_Xi_procs(void)` | 200 |
| `XOpenDisplay` | `Display* XOpenDisplay(const char* display_name)` | ~210 |
| `XCloseDisplay` | `int XCloseDisplay(Display* display)` | ~215 |
| `XFlush` | `int XFlush(Display* display)` | ~220 |
| `XNextEvent` | `int XNextEvent(Display* display, XEvent* event_return)` | ~225 |
| `XPending` | `int XPending(Display* display)` | ~230 |
| `XInitThreads` | `Status XInitThreads(void)` | ~235 |
| `XFilterEvent` | `Bool XFilterEvent(XEvent* event, Window w)` | ~240 |
| `XkbSetDetectableAutoRepeat` | `Bool XkbSetDetectableAutoRepeat(Display* display, Bool detectable, Bool* supported_rtrn)` | ~245 |
| `XSync` | `int XSync(Display* display, Bool discard)` | ~250 |
| `XrmInitialize` | `void XrmInitialize(void)` | ~255 |
| `XChangeProperty` | `int XChangeProperty(Display*, Window, Atom, Atom, int, int, const unsigned char*, int)` | ~260 |
| `XSendEvent` | `Status XSendEvent(Display*, Window, Bool, long, XEvent*)` | ~265 |
| `XFree` | `int XFree(void* data)` | ~270 |
| `XSetErrorHandler` | `XErrorHandler XSetErrorHandler(XErrorHandler handler)` | ~275 |

*(60+ additional X11 wrapper functions)*

---

### File: `shims/linux/gl.c` — OpenGL Dynamic Loading Shim
**Path:** `C:\cosmo-sokol\shims\linux\gl.c`

**ABI-CRITICAL:** Provides ~600 OpenGL function wrappers loaded via `cosmo_dlopen`.

| Key Functions | Signature | Line |
|---------------|-----------|------|
| `load_gl_procs` | `static void load_gl_procs(void)` | ~150 |
| `glClear` | `void glClear(GLbitfield mask)` | ~300 |
| `glCreateProgram` | `GLuint glCreateProgram(void)` | ~400 |
| `glCreateShader` | `GLuint glCreateShader(GLenum type)` | ~405 |
| `glCompileShader` | `void glCompileShader(GLuint shader)` | ~410 |
| `glLinkProgram` | `void glLinkProgram(GLuint program)` | ~500 |
| `glUseProgram` | `void glUseProgram(GLuint program)` | ~505 |
| `glDrawArrays` | `void glDrawArrays(GLenum mode, GLint first, GLsizei count)` | ~600 |
| `glDrawElements` | `void glDrawElements(GLenum mode, GLsizei count, GLenum type, const void* indices)` | ~605 |

*(~400 additional GL wrapper functions)*

---

## ABI Analysis — Critical Findings

### 1. Runtime Platform Dispatch Pattern

The core ABI strategy in cosmo-sokol is **runtime dispatch** rather than compile-time selection:

```c
// Example from sokol_cosmo.c
bool sapp_isvalid(void) {
    if (IsLinux()) {
        return linux_sapp_isvalid();
    }
    if (IsWindows()) {
        return windows_sapp_isvalid();
    }
    if (IsXnu()) {
        return macos_sapp_isvalid();
    }
}
```

**ABI Impact:** Each platform backend must have identical function signatures. The unified binary contains code for all platforms.

### 2. Dynamic Library Trampolines (Linux)

Linux shims use `cosmo_dltramp()` for function pointer calls:

```c
proc_XOpenDisplay = cosmo_dltramp(cosmo_dlsym(libX11, "XOpenDisplay"));
```

**ABI Impact:** `cosmo_dltramp()` handles calling convention translation between Cosmopolitan's unified ABI and native Linux x86_64 SysV ABI.

### 3. Windows Calling Convention

Windows shims properly define `WINAPI` for callbacks:

```c
typedef WINAPI int(*NvAPI_Initialize_t)(void);
#define APIENTRY WINAPI
#define WNDPROC NtWndProc
```

**ABI Impact:** Ensures Win64 calling convention compliance for Windows API callbacks.

### 4. Struct Return Value Handling

Multiple sokol functions return large structs by value:

```c
sg_desc sg_query_desc(void);          // Returns ~1KB struct
sg_features sg_query_features(void);   // Returns flags struct
sg_limits sg_query_limits(void);       // Returns limits struct
```

**ABI Impact:** On AMD64 SysV, structs > 16 bytes use hidden sret parameter. The dispatch layer must handle this identically across all platforms.

---

## Recommendations for Upstream Sync

### For floooh/sokol Sync:
1. Monitor `sokol_app.h` for new platform-specific functions
2. Any new `sapp_*` or `sg_*` functions need 3 implementations + dispatch wrapper
3. Watch for changes to struct sizes (ABI breaking)

### For jart/cosmopolitan Sync:
1. Monitor `cosmo_dltramp()` for any ABI changes
2. Track `IsLinux()`/`IsWindows()`/`IsXnu()` implementation
3. Watch for new platform detection functions

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Total Files Analyzed | 12 |
| Public API Functions (dispatch) | 120 |
| Platform-specific stubs (macos_*) | 90+ |
| X11 Wrapper Functions | 60+ |
| OpenGL Wrapper Functions | ~400 |
| Inline Assembly Blocks | **0** |
| Architecture-specific Code | **0** |

---

*Generated by asm specialist for Swiss Rounds v4 — Round 1*
