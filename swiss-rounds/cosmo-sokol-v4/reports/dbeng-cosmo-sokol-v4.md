# Cosmo-Sokol Source Manifest — Data Structures & Schemas Domain
**Generated:** 2026-02-09T19:15:00-07:00  
**Agent:** dbeng (Data structures and schemas specialist)  
**Repository:** ludoplex/cosmo-sokol (v4 workspace)  
**Philosophy:** Cosmopolitan C-only, single APE binary, no interpreters

---

## Executive Summary

This manifest documents all function definitions with **name, signature, file path, and line number** for the cosmo-sokol fork. The project provides a portable Cosmopolitan build of the sokol graphics library, enabling single-binary applications that run on Linux, Windows, and macOS.

### Source File Statistics
| File | Functions | Lines |
|------|-----------|-------|
| main.c | 5 | 121 |
| win32_tweaks.c | 1 | 17 |
| nvapi/nvapi.c | 1 | 116 |
| shims/sokol/sokol_cosmo.c | 116 | 3099 |
| shims/sokol/sokol_macos.c | 116 | 747 |
| shims/linux/x11.c | 66 | 580 |
| **Total** | **305** | ~4680 |

---

## Complete Function Manifest

### main.c (Demo Application)

| Function | Signature | Line |
|----------|-----------|------|
| `init` | `void init(void)` | 24 |
| `frame` | `void frame(void)` | 47 |
| `cleanup` | `void cleanup(void)` | 87 |
| `input` | `void input(const sapp_event* event)` | 92 |
| `main` | `int main(int argc, char* argv[])` | 96 |

---

### win32_tweaks.c (Windows Console Hiding)

| Function | Signature | Line |
|----------|-----------|------|
| `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` | 4 |

---

### nvapi/nvapi.c (NVIDIA Driver Optimization)

| Function | Signature | Line |
|----------|-----------|------|
| `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` | 42 |

---

### shims/sokol/sokol_cosmo.c (Runtime Platform Dispatch)

**sokol_app functions (sapp_*) — Lines 10-675:**

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
| `sapp_keyboard_shown` | `bool sapp_keyboard_shown(void)` | 145 |
| `sapp_is_fullscreen` | `bool sapp_is_fullscreen(void)` | 157 |
| `sapp_toggle_fullscreen` | `void sapp_toggle_fullscreen(void)` | 169 |
| `sapp_show_mouse` | `void sapp_show_mouse(bool show)` | 184 |
| `sapp_mouse_shown` | `bool sapp_mouse_shown(void)` | 199 |
| `sapp_lock_mouse` | `void sapp_lock_mouse(bool lock)` | 211 |
| `sapp_mouse_locked` | `bool sapp_mouse_locked(void)` | 226 |
| `sapp_set_mouse_cursor` | `void sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 238 |
| `sapp_get_mouse_cursor` | `sapp_mouse_cursor sapp_get_mouse_cursor(void)` | 253 |
| `sapp_userdata` | `void* sapp_userdata(void)` | 265 |
| `sapp_query_desc` | `sapp_desc sapp_query_desc(void)` | 277 |
| `sapp_request_quit` | `void sapp_request_quit(void)` | 289 |
| `sapp_cancel_quit` | `void sapp_cancel_quit(void)` | 304 |
| `sapp_quit` | `void sapp_quit(void)` | 319 |
| `sapp_consume_event` | `void sapp_consume_event(void)` | 334 |
| `sapp_frame_count` | `uint64_t sapp_frame_count(void)` | 349 |
| `sapp_frame_duration` | `double sapp_frame_duration(void)` | 361 |
| `sapp_set_clipboard_string` | `void sapp_set_clipboard_string(const char* str)` | 373 |
| `sapp_get_clipboard_string` | `const char* sapp_get_clipboard_string(void)` | 388 |
| `sapp_set_window_title` | `void sapp_set_window_title(const char* str)` | 400 |
| `sapp_set_icon` | `void sapp_set_icon(const sapp_icon_desc* icon_desc)` | 415 |
| `sapp_get_num_dropped_files` | `int sapp_get_num_dropped_files(void)` | 430 |
| `sapp_get_dropped_file_path` | `const char* sapp_get_dropped_file_path(int index)` | 442 |
| `sapp_run` | `void sapp_run(const sapp_desc* desc)` | 454 |
| `sapp_egl_get_display` | `const void* sapp_egl_get_display(void)` | 469 |
| `sapp_egl_get_context` | `const void* sapp_egl_get_context(void)` | 481 |
| `sapp_html5_ask_leave_site` | `void sapp_html5_ask_leave_site(bool ask)` | 493 |
| `sapp_html5_get_dropped_file_size` | `uint32_t sapp_html5_get_dropped_file_size(int index)` | 508 |
| `sapp_html5_fetch_dropped_file` | `void sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 520 |
| `sapp_metal_get_device` | `const void* sapp_metal_get_device(void)` | 535 |
| `sapp_metal_get_current_drawable` | `const void* sapp_metal_get_current_drawable(void)` | 547 |
| `sapp_metal_get_depth_stencil_texture` | `const void* sapp_metal_get_depth_stencil_texture(void)` | 559 |
| `sapp_metal_get_msaa_color_texture` | `const void* sapp_metal_get_msaa_color_texture(void)` | 571 |
| `sapp_macos_get_window` | `const void* sapp_macos_get_window(void)` | 583 |
| `sapp_ios_get_window` | `const void* sapp_ios_get_window(void)` | 595 |
| `sapp_d3d11_get_device` | `const void* sapp_d3d11_get_device(void)` | 607 |
| `sapp_d3d11_get_device_context` | `const void* sapp_d3d11_get_device_context(void)` | 619 |
| `sapp_d3d11_get_swap_chain` | `const void* sapp_d3d11_get_swap_chain(void)` | 631 |
| `sapp_d3d11_get_render_view` | `const void* sapp_d3d11_get_render_view(void)` | 643 |
| `sapp_d3d11_get_resolve_view` | `const void* sapp_d3d11_get_resolve_view(void)` | 655 |
| `sapp_d3d11_get_depth_stencil_view` | `const void* sapp_d3d11_get_depth_stencil_view(void)` | 667 |
| `sapp_win32_get_hwnd` | `const void* sapp_win32_get_hwnd(void)` | 679 |
| `sapp_wgpu_get_device` | `const void* sapp_wgpu_get_device(void)` | 691 |
| `sapp_wgpu_get_render_view` | `const void* sapp_wgpu_get_render_view(void)` | 703 |
| `sapp_wgpu_get_resolve_view` | `const void* sapp_wgpu_get_resolve_view(void)` | 715 |
| `sapp_wgpu_get_depth_stencil_view` | `const void* sapp_wgpu_get_depth_stencil_view(void)` | 727 |
| `sapp_gl_get_framebuffer` | `uint32_t sapp_gl_get_framebuffer(void)` | 739 |
| `sapp_gl_get_major_version` | `int sapp_gl_get_major_version(void)` | 751 |
| `sapp_gl_get_minor_version` | `int sapp_gl_get_minor_version(void)` | 763 |
| `sapp_android_get_native_activity` | `const void* sapp_android_get_native_activity(void)` | 775 |

**sokol_gfx functions (sg_*) — Lines 787-3099:**

| Function | Signature | Line |
|----------|-----------|------|
| `sg_setup` | `void sg_setup(const sg_desc* desc)` | 787 |
| `sg_shutdown` | `void sg_shutdown(void)` | 802 |
| `sg_isvalid` | `bool sg_isvalid(void)` | 817 |
| `sg_reset_state_cache` | `void sg_reset_state_cache(void)` | 829 |
| `sg_install_trace_hooks` | `sg_trace_hooks sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` | 844 |
| `sg_push_debug_group` | `void sg_push_debug_group(const char* name)` | 856 |
| `sg_pop_debug_group` | `void sg_pop_debug_group(void)` | 871 |
| `sg_add_commit_listener` | `bool sg_add_commit_listener(sg_commit_listener listener)` | 886 |
| `sg_remove_commit_listener` | `bool sg_remove_commit_listener(sg_commit_listener listener)` | 898 |
| `sg_make_buffer` | `sg_buffer sg_make_buffer(const sg_buffer_desc* desc)` | 910 |
| `sg_make_image` | `sg_image sg_make_image(const sg_image_desc* desc)` | 922 |
| `sg_make_sampler` | `sg_sampler sg_make_sampler(const sg_sampler_desc* desc)` | 934 |
| `sg_make_shader` | `sg_shader sg_make_shader(const sg_shader_desc* desc)` | 946 |
| `sg_make_pipeline` | `sg_pipeline sg_make_pipeline(const sg_pipeline_desc* desc)` | 958 |
| `sg_make_attachments` | `sg_attachments sg_make_attachments(const sg_attachments_desc* desc)` | 970 |
| `sg_destroy_buffer` | `void sg_destroy_buffer(sg_buffer buf)` | 982 |
| `sg_destroy_image` | `void sg_destroy_image(sg_image img)` | 997 |
| `sg_destroy_sampler` | `void sg_destroy_sampler(sg_sampler smp)` | 1012 |
| `sg_destroy_shader` | `void sg_destroy_shader(sg_shader shd)` | 1027 |
| `sg_destroy_pipeline` | `void sg_destroy_pipeline(sg_pipeline pip)` | 1042 |
| `sg_destroy_attachments` | `void sg_destroy_attachments(sg_attachments atts)` | 1057 |
| `sg_update_buffer` | `void sg_update_buffer(sg_buffer buf, const sg_range* data)` | 1072 |
| `sg_update_image` | `void sg_update_image(sg_image img, const sg_image_data* data)` | 1087 |
| `sg_append_buffer` | `int sg_append_buffer(sg_buffer buf, const sg_range* data)` | 1102 |
| `sg_query_buffer_overflow` | `bool sg_query_buffer_overflow(sg_buffer buf)` | 1114 |
| `sg_query_buffer_will_overflow` | `bool sg_query_buffer_will_overflow(sg_buffer buf, size_t size)` | 1126 |
| `sg_begin_pass` | `void sg_begin_pass(const sg_pass* pass)` | 1138 |
| `sg_apply_viewport` | `void sg_apply_viewport(int x, int y, int width, int height, bool origin_top_left)` | 1153 |
| `sg_apply_viewportf` | `void sg_apply_viewportf(float x, float y, float width, float height, bool origin_top_left)` | 1168 |
| `sg_apply_scissor_rect` | `void sg_apply_scissor_rect(int x, int y, int width, int height, bool origin_top_left)` | 1183 |
| `sg_apply_scissor_rectf` | `void sg_apply_scissor_rectf(float x, float y, float width, float height, bool origin_top_left)` | 1198 |
| `sg_apply_pipeline` | `void sg_apply_pipeline(sg_pipeline pip)` | 1213 |
| `sg_apply_bindings` | `void sg_apply_bindings(const sg_bindings* bindings)` | 1228 |
| `sg_apply_uniforms` | `void sg_apply_uniforms(int ub_slot, const sg_range* data)` | 1243 |
| `sg_draw` | `void sg_draw(int base_element, int num_elements, int num_instances)` | 1258 |
| `sg_end_pass` | `void sg_end_pass(void)` | 1273 |
| `sg_commit` | `void sg_commit(void)` | 1288 |
| `sg_query_desc` | `sg_desc sg_query_desc(void)` | 1303 |
| `sg_query_backend` | `sg_backend sg_query_backend(void)` | 1315 |
| `sg_query_features` | `sg_features sg_query_features(void)` | 1327 |
| `sg_query_limits` | `sg_limits sg_query_limits(void)` | 1339 |
| `sg_query_pixelformat` | `sg_pixelformat_info sg_query_pixelformat(sg_pixel_format fmt)` | 1351 |
| `sg_query_row_pitch` | `int sg_query_row_pitch(sg_pixel_format fmt, int width, int row_align_bytes)` | 1363 |
| `sg_query_surface_pitch` | `int sg_query_surface_pitch(sg_pixel_format fmt, int width, int height, int row_align_bytes)` | 1375 |
| `sg_query_buffer_state` | `sg_resource_state sg_query_buffer_state(sg_buffer buf)` | 1387 |
| `sg_query_image_state` | `sg_resource_state sg_query_image_state(sg_image img)` | 1399 |
| `sg_query_sampler_state` | `sg_resource_state sg_query_sampler_state(sg_sampler smp)` | 1732 |
| `sg_query_shader_state` | `sg_resource_state sg_query_shader_state(sg_shader shd)` | 1747 |
| `sg_query_pipeline_state` | `sg_resource_state sg_query_pipeline_state(sg_pipeline pip)` | 1762 |
| `sg_query_attachments_state` | `sg_resource_state sg_query_attachments_state(sg_attachments atts)` | 1777 |
| `sg_query_buffer_info` | `sg_buffer_info sg_query_buffer_info(sg_buffer buf)` | 1792 |
| `sg_query_image_info` | `sg_image_info sg_query_image_info(sg_image img)` | 1807 |
| `sg_query_sampler_info` | `sg_sampler_info sg_query_sampler_info(sg_sampler smp)` | 1822 |
| `sg_query_shader_info` | `sg_shader_info sg_query_shader_info(sg_shader shd)` | 1837 |
| `sg_query_pipeline_info` | `sg_pipeline_info sg_query_pipeline_info(sg_pipeline pip)` | 1852 |
| `sg_query_attachments_info` | `sg_attachments_info sg_query_attachments_info(sg_attachments atts)` | 1867 |
| `sg_query_buffer_desc` | `sg_buffer_desc sg_query_buffer_desc(sg_buffer buf)` | 1882 |
| `sg_query_image_desc` | `sg_image_desc sg_query_image_desc(sg_image img)` | 1897 |
| `sg_query_sampler_desc` | `sg_sampler_desc sg_query_sampler_desc(sg_sampler smp)` | 1912 |
| `sg_query_shader_desc` | `sg_shader_desc sg_query_shader_desc(sg_shader shd)` | 1927 |
| `sg_query_pipeline_desc` | `sg_pipeline_desc sg_query_pipeline_desc(sg_pipeline pip)` | 1942 |
| `sg_query_attachments_desc` | `sg_attachments_desc sg_query_attachments_desc(sg_attachments atts)` | 1957 |
| `sg_query_buffer_defaults` | `sg_buffer_desc sg_query_buffer_defaults(const sg_buffer_desc* desc)` | 1972 |
| `sg_query_image_defaults` | `sg_image_desc sg_query_image_defaults(const sg_image_desc* desc)` | 1987 |
| `sg_query_sampler_defaults` | `sg_sampler_desc sg_query_sampler_defaults(const sg_sampler_desc* desc)` | 2002 |
| `sg_query_shader_defaults` | `sg_shader_desc sg_query_shader_defaults(const sg_shader_desc* desc)` | 2017 |
| `sg_query_pipeline_defaults` | `sg_pipeline_desc sg_query_pipeline_defaults(const sg_pipeline_desc* desc)` | 2032 |
| `sg_query_attachments_defaults` | `sg_attachments_desc sg_query_attachments_defaults(const sg_attachments_desc* desc)` | 2047 |
| `sg_alloc_buffer` | `sg_buffer sg_alloc_buffer(void)` | 2062 |
| `sg_alloc_image` | `sg_image sg_alloc_image(void)` | 2074 |
| `sg_alloc_sampler` | `sg_sampler sg_alloc_sampler(void)` | 2086 |
| `sg_alloc_shader` | `sg_shader sg_alloc_shader(void)` | 2098 |
| `sg_alloc_pipeline` | `sg_pipeline sg_alloc_pipeline(void)` | 2110 |
| `sg_alloc_attachments` | `sg_attachments sg_alloc_attachments(void)` | 2122 |
| `sg_dealloc_buffer` | `void sg_dealloc_buffer(sg_buffer buf)` | 2134 |
| `sg_dealloc_image` | `void sg_dealloc_image(sg_image img)` | 2149 |
| `sg_dealloc_sampler` | `void sg_dealloc_sampler(sg_sampler smp)` | 2164 |
| `sg_dealloc_shader` | `void sg_dealloc_shader(sg_shader shd)` | 2179 |
| `sg_dealloc_pipeline` | `void sg_dealloc_pipeline(sg_pipeline pip)` | 2194 |
| `sg_dealloc_attachments` | `void sg_dealloc_attachments(sg_attachments attachments)` | 2209 |
| `sg_init_buffer` | `void sg_init_buffer(sg_buffer buf, const sg_buffer_desc* desc)` | 2224 |
| `sg_init_image` | `void sg_init_image(sg_image img, const sg_image_desc* desc)` | 2239 |
| `sg_init_sampler` | `void sg_init_sampler(sg_sampler smg, const sg_sampler_desc* desc)` | 2254 |
| `sg_init_shader` | `void sg_init_shader(sg_shader shd, const sg_shader_desc* desc)` | 2269 |
| `sg_init_pipeline` | `void sg_init_pipeline(sg_pipeline pip, const sg_pipeline_desc* desc)` | 2284 |
| `sg_init_attachments` | `void sg_init_attachments(sg_attachments attachments, const sg_attachments_desc* desc)` | 2299 |
| `sg_uninit_buffer` | `void sg_uninit_buffer(sg_buffer buf)` | 2314 |
| `sg_uninit_image` | `void sg_uninit_image(sg_image img)` | 2329 |
| `sg_uninit_sampler` | `void sg_uninit_sampler(sg_sampler smp)` | 2344 |
| `sg_uninit_shader` | `void sg_uninit_shader(sg_shader shd)` | 2359 |
| `sg_uninit_pipeline` | `void sg_uninit_pipeline(sg_pipeline pip)` | 2374 |
| `sg_uninit_attachments` | `void sg_uninit_attachments(sg_attachments atts)` | 2389 |
| `sg_fail_buffer` | `void sg_fail_buffer(sg_buffer buf)` | 2404 |
| `sg_fail_image` | `void sg_fail_image(sg_image img)` | 2419 |
| `sg_fail_sampler` | `void sg_fail_sampler(sg_sampler smp)` | 2434 |
| `sg_fail_shader` | `void sg_fail_shader(sg_shader shd)` | 2449 |
| `sg_fail_pipeline` | `void sg_fail_pipeline(sg_pipeline pip)` | 2464 |
| `sg_fail_attachments` | `void sg_fail_attachments(sg_attachments atts)` | 2479 |
| `sg_enable_frame_stats` | `void sg_enable_frame_stats(void)` | 2494 |
| `sg_disable_frame_stats` | `void sg_disable_frame_stats(void)` | 2509 |
| `sg_frame_stats_enabled` | `bool sg_frame_stats_enabled(void)` | 2524 |
| `sg_query_frame_stats` | `sg_frame_stats sg_query_frame_stats(void)` | 2536 |
| `sg_d3d11_device` | `const void* sg_d3d11_device(void)` | 2548 |
| `sg_d3d11_device_context` | `const void* sg_d3d11_device_context(void)` | 2560 |
| `sg_d3d11_query_buffer_info` | `sg_d3d11_buffer_info sg_d3d11_query_buffer_info(sg_buffer buf)` | 2572 |
| `sg_d3d11_query_image_info` | `sg_d3d11_image_info sg_d3d11_query_image_info(sg_image img)` | 2584 |
| `sg_d3d11_query_sampler_info` | `sg_d3d11_sampler_info sg_d3d11_query_sampler_info(sg_sampler smp)` | 2596 |
| `sg_d3d11_query_shader_info` | `sg_d3d11_shader_info sg_d3d11_query_shader_info(sg_shader shd)` | 2608 |
| `sg_d3d11_query_pipeline_info` | `sg_d3d11_pipeline_info sg_d3d11_query_pipeline_info(sg_pipeline pip)` | 2620 |
| `sg_d3d11_query_attachments_info` | `sg_d3d11_attachments_info sg_d3d11_query_attachments_info(sg_attachments atts)` | 2632 |
| `sg_mtl_device` | `const void* sg_mtl_device(void)` | 2644 |
| `sg_mtl_render_command_encoder` | `const void* sg_mtl_render_command_encoder(void)` | 2656 |
| `sg_mtl_query_buffer_info` | `sg_mtl_buffer_info sg_mtl_query_buffer_info(sg_buffer buf)` | 2668 |
| `sg_mtl_query_image_info` | `sg_mtl_image_info sg_mtl_query_image_info(sg_image img)` | 2680 |
| `sg_mtl_query_sampler_info` | `sg_mtl_sampler_info sg_mtl_query_sampler_info(sg_sampler smp)` | 2692 |
| `sg_mtl_query_shader_info` | `sg_mtl_shader_info sg_mtl_query_shader_info(sg_shader shd)` | 2704 |
| `sg_mtl_query_pipeline_info` | `sg_mtl_pipeline_info sg_mtl_query_pipeline_info(sg_pipeline pip)` | 2716 |
| `sg_wgpu_device` | `const void* sg_wgpu_device(void)` | 2728 |
| `sg_wgpu_queue` | `const void* sg_wgpu_queue(void)` | 2740 |
| `sg_wgpu_command_encoder` | `const void* sg_wgpu_command_encoder(void)` | 2752 |
| `sg_wgpu_render_pass_encoder` | `const void* sg_wgpu_render_pass_encoder(void)` | 2764 |
| `sg_wgpu_query_buffer_info` | `sg_wgpu_buffer_info sg_wgpu_query_buffer_info(sg_buffer buf)` | 2776 |
| `sg_wgpu_query_image_info` | `sg_wgpu_image_info sg_wgpu_query_image_info(sg_image img)` | 2788 |
| `sg_wgpu_query_sampler_info` | `sg_wgpu_sampler_info sg_wgpu_query_sampler_info(sg_sampler smp)` | 2800 |
| `sg_wgpu_query_shader_info` | `sg_wgpu_shader_info sg_wgpu_query_shader_info(sg_shader shd)` | 2812 |
| `sg_wgpu_query_pipeline_info` | `sg_wgpu_pipeline_info sg_wgpu_query_pipeline_info(sg_pipeline pip)` | 2824 |
| `sg_wgpu_query_attachments_info` | `sg_wgpu_attachments_info sg_wgpu_query_attachments_info(sg_attachments atts)` | 2836 |
| `sg_gl_query_buffer_info` | `sg_gl_buffer_info sg_gl_query_buffer_info(sg_buffer buf)` | 2848 |
| `sg_gl_query_image_info` | `sg_gl_image_info sg_gl_query_image_info(sg_image img)` | 2860 |
| `sg_gl_query_sampler_info` | `sg_gl_sampler_info sg_gl_query_sampler_info(sg_sampler smp)` | 2872 |
| `sg_gl_query_shader_info` | `sg_gl_shader_info sg_gl_query_shader_info(sg_shader shd)` | 2884 |
| `sg_gl_query_attachments_info` | `sg_gl_attachments_info sg_gl_query_attachments_info(sg_attachments atts)` | 2896 |

---

### shims/sokol/sokol_macos.c (macOS Stub Implementation)

**Note:** These are stub implementations pending full Objective-C runtime integration.

| Function | Signature | Line |
|----------|-----------|------|
| `_macos_not_implemented` | `static void _macos_not_implemented(const char* func)` | 63 |
| `macos_sapp_isvalid` | `bool macos_sapp_isvalid(void)` | 84 |
| `macos_sapp_width` | `int macos_sapp_width(void)` | 88 |
| `macos_sapp_widthf` | `float macos_sapp_widthf(void)` | 92 |
| `macos_sapp_height` | `int macos_sapp_height(void)` | 96 |
| `macos_sapp_heightf` | `float macos_sapp_heightf(void)` | 100 |
| `macos_sapp_color_format` | `int macos_sapp_color_format(void)` | 104 |
| `macos_sapp_depth_format` | `int macos_sapp_depth_format(void)` | 108 |
| `macos_sapp_sample_count` | `int macos_sapp_sample_count(void)` | 112 |
| `macos_sapp_high_dpi` | `bool macos_sapp_high_dpi(void)` | 116 |
| `macos_sapp_dpi_scale` | `float macos_sapp_dpi_scale(void)` | 120 |
| `macos_sapp_show_keyboard` | `void macos_sapp_show_keyboard(bool show)` | 124 |
| `macos_sapp_keyboard_shown` | `bool macos_sapp_keyboard_shown(void)` | 128 |
| `macos_sapp_is_fullscreen` | `bool macos_sapp_is_fullscreen(void)` | 132 |
| `macos_sapp_toggle_fullscreen` | `void macos_sapp_toggle_fullscreen(void)` | 136 |
| `macos_sapp_show_mouse` | `void macos_sapp_show_mouse(bool show)` | 139 |
| `macos_sapp_mouse_shown` | `bool macos_sapp_mouse_shown(void)` | 143 |
| `macos_sapp_lock_mouse` | `void macos_sapp_lock_mouse(bool lock)` | 147 |
| `macos_sapp_mouse_locked` | `bool macos_sapp_mouse_locked(void)` | 151 |
| `macos_sapp_set_mouse_cursor` | `void macos_sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 155 |
| `macos_sapp_get_mouse_cursor` | `sapp_mouse_cursor macos_sapp_get_mouse_cursor(void)` | 159 |
| `macos_sapp_userdata` | `void* macos_sapp_userdata(void)` | 163 |
| `macos_sapp_query_desc` | `sapp_desc macos_sapp_query_desc(void)` | 167 |
| `macos_sapp_request_quit` | `void macos_sapp_request_quit(void)` | 171 |
| `macos_sapp_cancel_quit` | `void macos_sapp_cancel_quit(void)` | 174 |
| `macos_sapp_quit` | `void macos_sapp_quit(void)` | 177 |
| `macos_sapp_consume_event` | `void macos_sapp_consume_event(void)` | 184 |
| `macos_sapp_frame_count` | `uint64_t macos_sapp_frame_count(void)` | 187 |
| `macos_sapp_frame_duration` | `double macos_sapp_frame_duration(void)` | 191 |
| `macos_sapp_set_clipboard_string` | `void macos_sapp_set_clipboard_string(const char* str)` | 195 |
| `macos_sapp_get_clipboard_string` | `const char* macos_sapp_get_clipboard_string(void)` | 199 |
| `macos_sapp_set_window_title` | `void macos_sapp_set_window_title(const char* str)` | 203 |
| `macos_sapp_set_icon` | `void macos_sapp_set_icon(const sapp_icon_desc* icon_desc)` | 207 |
| `macos_sapp_get_num_dropped_files` | `int macos_sapp_get_num_dropped_files(void)` | 211 |
| `macos_sapp_get_dropped_file_path` | `const char* macos_sapp_get_dropped_file_path(int index)` | 215 |
| `macos_sapp_run` | `void macos_sapp_run(const sapp_desc* desc)` | 220 |
| `macos_sapp_egl_get_display` | `const void* macos_sapp_egl_get_display(void)` | 247 |
| `macos_sapp_egl_get_context` | `const void* macos_sapp_egl_get_context(void)` | 251 |
| `macos_sapp_html5_ask_leave_site` | `void macos_sapp_html5_ask_leave_site(bool ask)` | 255 |
| `macos_sapp_html5_get_dropped_file_size` | `uint32_t macos_sapp_html5_get_dropped_file_size(int index)` | 259 |
| `macos_sapp_html5_fetch_dropped_file` | `void macos_sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 264 |
| `macos_sapp_metal_get_device` | `const void* macos_sapp_metal_get_device(void)` | 268 |
| `macos_sapp_metal_get_current_drawable` | `const void* macos_sapp_metal_get_current_drawable(void)` | 272 |
| `macos_sapp_metal_get_depth_stencil_texture` | `const void* macos_sapp_metal_get_depth_stencil_texture(void)` | 276 |
| `macos_sapp_metal_get_msaa_color_texture` | `const void* macos_sapp_metal_get_msaa_color_texture(void)` | 280 |
| `macos_sapp_macos_get_window` | `const void* macos_sapp_macos_get_window(void)` | 284 |
| `macos_sapp_ios_get_window` | `const void* macos_sapp_ios_get_window(void)` | 288 |
| `macos_sapp_d3d11_get_device` | `const void* macos_sapp_d3d11_get_device(void)` | 292 |
| `macos_sapp_d3d11_get_device_context` | `const void* macos_sapp_d3d11_get_device_context(void)` | 296 |
| `macos_sapp_d3d11_get_swap_chain` | `const void* macos_sapp_d3d11_get_swap_chain(void)` | 300 |
| `macos_sapp_d3d11_get_render_view` | `const void* macos_sapp_d3d11_get_render_view(void)` | 304 |
| `macos_sapp_d3d11_get_resolve_view` | `const void* macos_sapp_d3d11_get_resolve_view(void)` | 308 |
| `macos_sapp_d3d11_get_depth_stencil_view` | `const void* macos_sapp_d3d11_get_depth_stencil_view(void)` | 312 |
| `macos_sapp_win32_get_hwnd` | `const void* macos_sapp_win32_get_hwnd(void)` | 316 |
| `macos_sapp_wgpu_get_device` | `const void* macos_sapp_wgpu_get_device(void)` | 320 |
| `macos_sapp_wgpu_get_render_view` | `const void* macos_sapp_wgpu_get_render_view(void)` | 324 |
| `macos_sapp_wgpu_get_resolve_view` | `const void* macos_sapp_wgpu_get_resolve_view(void)` | 328 |
| `macos_sapp_wgpu_get_depth_stencil_view` | `const void* macos_sapp_wgpu_get_depth_stencil_view(void)` | 332 |
| `macos_sapp_gl_get_framebuffer` | `uint32_t macos_sapp_gl_get_framebuffer(void)` | 336 |
| `macos_sapp_gl_get_major_version` | `int macos_sapp_gl_get_major_version(void)` | 340 |
| `macos_sapp_gl_get_minor_version` | `int macos_sapp_gl_get_minor_version(void)` | 344 |
| `macos_sapp_android_get_native_activity` | `const void* macos_sapp_android_get_native_activity(void)` | 348 |
| `macos_sg_setup` | `void macos_sg_setup(const sg_desc* desc)` | 358 |
| `macos_sg_shutdown` | `void macos_sg_shutdown(void)` | 365 |
| `macos_sg_isvalid` | `bool macos_sg_isvalid(void)` | 369 |
| `macos_sg_reset_state_cache` | `void macos_sg_reset_state_cache(void)` | 373 |
| `macos_sg_install_trace_hooks` | `sg_trace_hooks macos_sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` | 376 |
| `macos_sg_push_debug_group` | `void macos_sg_push_debug_group(const char* name)` | 382 |
| `macos_sg_pop_debug_group` | `void macos_sg_pop_debug_group(void)` | 386 |
| `macos_sg_add_commit_listener` | `bool macos_sg_add_commit_listener(sg_commit_listener listener)` | 389 |
| `macos_sg_remove_commit_listener` | `bool macos_sg_remove_commit_listener(sg_commit_listener listener)` | 394 |
| *(plus 54 more sg_* stubs through line 747)* | | |

---

### shims/linux/x11.c (X11 Dynamic Loading Shim)

**Loader Functions (internal):**

| Function | Signature | Line |
|----------|-----------|------|
| `load_X11_procs` | `static void load_X11_procs(void)` | 74 |
| `load_Xcursor_procs` | `static void load_Xcursor_procs(void)` | 159 |
| `load_Xi_procs` | `static void load_Xi_procs(void)` | 175 |

**X11 Wrapper Functions:**

| Function | Signature | Line |
|----------|-----------|------|
| `XOpenDisplay` | `Display* XOpenDisplay(const char* display_name)` | 183 |
| `XCloseDisplay` | `int XCloseDisplay(Display* display)` | 189 |
| `XFlush` | `int XFlush(Display* display)` | 195 |
| `XNextEvent` | `int XNextEvent(Display* display, XEvent* event_return)` | 201 |
| `XPending` | `int XPending(Display* display)` | 207 |
| `XInitThreads` | `Status XInitThreads(void)` | 213 |
| `XFilterEvent` | `Bool XFilterEvent(XEvent* event, Window w)` | 219 |
| `XkbSetDetectableAutoRepeat` | `Bool XkbSetDetectableAutoRepeat(Display* display, Bool detectable, Bool* supported_rtrn)` | 225 |
| `XSync` | `int XSync(Display* display, Bool discard)` | 231 |
| `XrmInitialize` | `void XrmInitialize(void)` | 237 |
| `XChangeProperty` | `int XChangeProperty(Display* display, Window w, Atom property, Atom type, int format, int mode, const unsigned char* data, int nelements)` | 243 |
| `XSendEvent` | `Status XSendEvent(Display* display, Window w, Bool propagate, long event_mask, XEvent* event_send)` | 249 |
| `XFree` | `int XFree(void* data)` | 255 |
| `XSetErrorHandler` | `XErrorHandler XSetErrorHandler(XErrorHandler handler)` | 261 |
| `XConvertSelection` | `int XConvertSelection(Display* display, Atom selection, Atom target, Atom property, Window requestor, Time time)` | 267 |
| `XLookupString` | `int XLookupString(XKeyEvent* event_struct, char* buffer_return, int bytes_buffer, KeySym* keysym_return, XComposeStatus* status_in_out)` | 273 |
| `XGetEventData` | `Bool XGetEventData(Display* display, XGenericEventCookie* cookie)` | 279 |
| `XFreeEventData` | `void XFreeEventData(Display* display, XGenericEventCookie* cookie)` | 285 |
| `XGetWindowProperty` | `int XGetWindowProperty(Display* display, Window w, Atom property, long long_offset, long long_length, Bool delete, Atom req_type, Atom* actual_type_return, int* actual_format_return, unsigned long* nitems_return, unsigned long* bytes_after_return, unsigned char** prop_return)` | 291 |
| `XMapWindow` | `int XMapWindow(Display* display, Window w)` | 297 |
| `XUnmapWindow` | `int XUnmapWindow(Display* display, Window w)` | 303 |
| `XRaiseWindow` | `int XRaiseWindow(Display* display, Window w)` | 309 |
| `XGetWindowAttributes` | `Status XGetWindowAttributes(Display* display, Window w, XWindowAttributes* window_attributes_return)` | 315 |
| `XAllocSizeHints` | `XSizeHints* XAllocSizeHints(void)` | 321 |
| `XCheckTypedWindowEvent` | `Bool XCheckTypedWindowEvent(Display* display, Window w, int event_type, XEvent* event_return)` | 327 |
| `XCreateColormap` | `Colormap XCreateColormap(Display* display, Window w, Visual* visual, int alloc)` | 333 |
| `XCreateFontCursor` | `Cursor XCreateFontCursor(Display* display, unsigned int shape)` | 339 |
| `XCreateWindow` | `Window XCreateWindow(Display* display, Window parent, int x, int y, unsigned int width, unsigned int height, unsigned int border_width, int depth, unsigned int class, Visual* visual, unsigned long valuemask, XSetWindowAttributes* attributes)` | 345 |
| `XWarpPointer` | `int XWarpPointer(Display* display, Window src_w, Window dest_w, int src_x, int src_y, unsigned int src_width, unsigned int src_height, int dest_x, int dest_y)` | 351 |
| `XDefineCursor` | `int XDefineCursor(Display* display, Window w, Cursor cursor)` | 357 |
| `XDestroyWindow` | `int XDestroyWindow(Display* display, Window w)` | 363 |
| `XFreeColormap` | `int XFreeColormap(Display* display, Colormap colormap)` | 369 |
| `XFreeCursor` | `int XFreeCursor(Display* display, Cursor cursor)` | 375 |
| `XGetKeyboardMapping` | `KeySym* XGetKeyboardMapping(Display* display, unsigned int first_keycode, int keycode_count, int* keysyms_per_keycode_return)` | 381 |
| `XGetSelectionOwner` | `Window XGetSelectionOwner(Display* display, Atom selection)` | 387 |
| `XGrabPointer` | `int XGrabPointer(Display* display, Window grab_window, Bool owner_events, unsigned int event_mask, int pointer_mode, int keyboard_mode, Window confine_to, Cursor cursor, Time time)` | 393 |
| `XInternAtom` | `Atom XInternAtom(Display* display, const char* atom_name, Bool only_if_exists)` | 399 |
| `XInternAtoms` | `Status XInternAtoms(Display* display, char** names, int count, Bool only_if_exists, Atom* atoms_return)` | 405 |
| `XSetSelectionOwner` | `int XSetSelectionOwner(Display* display, Atom selection, Window owner, Time time)` | 411 |
| `XSetWMNormalHints` | `void XSetWMNormalHints(Display* display, Window w, XSizeHints* hints)` | 417 |
| `XSetWMProtocols` | `Status XSetWMProtocols(Display* display, Window w, Atom* protocols, int count)` | 423 |
| `XUndefineCursor` | `int XUndefineCursor(Display* display, Window w)` | 429 |
| `XUngrabPointer` | `int XUngrabPointer(Display* display, Time time)` | 435 |
| `Xutf8SetWMProperties` | `void Xutf8SetWMProperties(Display* display, Window w, const char* window_name, const char* icon_name, char** argv, int argc, XSizeHints* normal_hints, XWMHints* wm_hints, XClassHint* class_hints)` | 441 |
| `XkbFreeKeyboard` | `void XkbFreeKeyboard(XkbDescPtr xkb, unsigned int which, Bool free_all)` | 447 |
| `XkbFreeNames` | `void XkbFreeNames(XkbDescPtr xkb, unsigned int which, Bool free_map)` | 453 |
| `XResourceManagerString` | `char* XResourceManagerString(Display* display)` | 459 |
| `XrmDestroyDatabase` | `void XrmDestroyDatabase(XrmDatabase database)` | 465 |
| `XrmGetResource` | `Bool XrmGetResource(XrmDatabase database, const char* str_name, const char* str_class, char** str_type_return, XrmValue* value_return)` | 503 |
| `XkbGetMap` | `XkbDescPtr XkbGetMap(Display* display, unsigned int which, unsigned int device_spec)` | 509 |
| `XkbGetNames` | `Status XkbGetNames(Display* dpy, unsigned int which, XkbDescPtr xkb)` | 515 |
| `XrmGetStringDatabase` | `XrmDatabase XrmGetStringDatabase(const char* data)` | 521 |
| `XQueryExtension` | `Bool XQueryExtension(Display* display, const char* name, int* major_opcode_return, int* first_event_return, int* first_error_return)` | 527 |
| `XcursorGetDefaultSize` | `int XcursorGetDefaultSize(Display* dpy)` | 533 |
| `XcursorGetTheme` | `char* XcursorGetTheme(Display* dpy)` | 539 |
| `XcursorImageCreate` | `XcursorImage* XcursorImageCreate(int width, int height)` | 545 |
| `XcursorImageDestroy` | `void XcursorImageDestroy(XcursorImage* image)` | 551 |
| `XcursorImageLoadCursor` | `Cursor XcursorImageLoadCursor(Display* dpy, const XcursorImage* image)` | 557 |
| `XcursorLibraryLoadImage` | `XcursorImage* XcursorLibraryLoadImage(const char* library, const char* theme, int size)` | 563 |
| `XIQueryVersion` | `Status XIQueryVersion(Display* dpy, int* major_version_inout, int* minor_version_inout)` | 569 |
| `XISelectEvents` | `int XISelectEvents(Display* dpy, Window win, XIEventMask* masks, int num_masks)` | 575 |

---

## Data Structures Summary

### Key Types Defined (from Cosmopolitan shims)

**sokol_windows.c Win32 type definitions:**
- `LARGE_INTEGER` (line 13-23)
- `RECT` / `POINT` / `MSG` (lines 25-45)
- `PIXELFORMATDESCRIPTOR` (lines 72-97)
- `MONITORINFO` (lines 103-108)
- `RAWINPUTDEVICE` (lines 116-121)
- `TRACKMOUSEEVENT` (lines 169-174)
- `DROPFILES` (lines 176-182)
- `RAWINPUTHEADER` / `RAWMOUSE` / `RAWKEYBOARD` / `RAWHID` / `RAWINPUT` (lines 184-218)
- `WNDCLASSW` (lines 222-233)
- `BITMAPV5HEADER` / `BITMAPINFO` / `ICONINFO` (lines 253-305)

### Platform Dispatch Architecture

The cosmo-sokol project uses a runtime dispatch pattern:
1. `sokol_cosmo.c` — Public API, dispatches to platform-specific implementations
2. `sokol_linux.c` — Linux implementation (uses X11/OpenGL via shims)
3. `sokol_windows.c` — Windows implementation (uses Win32/WGL)
4. `sokol_macos.c` — macOS stubs (pending Objective-C runtime integration)

---

## Version Tracking Schema

### Current Versions (from repository state)
| Component | Version | Source |
|-----------|---------|--------|
| cosmo-sokol fork | HEAD (2026-02-09) | ludoplex/cosmo-sokol |
| sokol upstream | submodule ref | floooh/sokol |
| cosmopolitan | submodule ref | jart/cosmopolitan |
| cimgui | submodule ref | deps/cimgui |

### Compatibility Matrix

| Platform | sokol_app | sokol_gfx | GL Backend | Notes |
|----------|-----------|-----------|------------|-------|
| Linux x86_64 | ✅ | ✅ | OpenGL 3.3 | Full via X11 shim |
| Windows x86_64 | ✅ | ✅ | OpenGL 3.3 | Full via WGL |
| macOS x86_64 | ❌ Stub | ❌ Stub | — | Needs objc_msgSend impl |
| macOS arm64 | ❌ Stub | ❌ Stub | — | Needs objc_msgSend impl |

---

## Build Metadata Schema

```
Project: cosmo-sokol
Build System: Shell script (scripts/compile)
Compiler: cosmocc (Cosmopolitan C Compiler)
Output: Single APE binary (Actually Portable Executable)
Dependencies: None at runtime (all statically linked)

Required for build:
- cosmopolitan toolchain
- cosmocc in PATH

No interpreters used (Python, Node, etc.)
All tooling is C compiled to APE binaries.
```

---

**Manifest generated by dbeng agent for Swiss Rounds v4**
