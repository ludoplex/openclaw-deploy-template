# CI/CD Analysis Report: cosmo-sokol

**Domain:** CI/CD workflows (GitHub Actions, automated testing, release automation)  
**Generated:** 2026-02-09  
**Repository:** ludoplex/cosmo-sokol (fork)

---

## Executive Summary

cosmo-sokol is a Cosmopolitan build of the Sokol graphics library, producing **single portable APE binaries** that run on Windows, Linux, and macOS. The project follows the Cosmopolitan philosophy: **NO Python, NO Node, NO interpreters** — all tooling is pure C compiled with cosmocc.

### Current CI/CD Status
- ✅ GitHub Actions workflow exists (`.github/workflows/build.yml`)
- ✅ Build on push with cosmocc 3.9.6
- ✅ Automatic release drafting on tags
- ⚠️ No automated testing
- ⚠️ No upstream sync automation
- ⚠️ macOS backend is stub (not functional)

---

## Source Manifest

### File: `main.c`
| Line | Function Name | Signature |
|------|--------------|-----------|
| 24 | `init` | `void init(void)` |
| 45 | `frame` | `void frame(void)` |
| 84 | `cleanup` | `void cleanup(void)` |
| 89 | `input` | `void input(const sapp_event* event)` |
| 93 | `main` | `int main(int argc, char* argv[])` |

### File: `win32_tweaks.c`
| Line | Function Name | Signature |
|------|--------------|-----------|
| 4 | `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` |

### File: `win32_tweaks.h`
| Line | Function Name | Signature |
|------|--------------|-----------|
| 4 | `win32_tweaks_hide_console` | `void win32_tweaks_hide_console(void)` (declaration) |

### File: `nvapi/nvapi.c`
| Line | Function Name | Signature |
|------|--------------|-----------|
| 42 | `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` |

### File: `nvapi/nvapi.h`
| Line | Function Name | Signature |
|------|--------------|-----------|
| 6 | `nvapi_disable_threaded_optimization` | `bool nvapi_disable_threaded_optimization(const char* profile_name)` (declaration) |

### File: `shims/sokol/sokol_shared.c`
*Configuration file - includes sokol headers with SOKOL_IMPL*

| Line | Component | Description |
|------|-----------|-------------|
| 1 | `SOKOL_NO_ENTRY` | Disable sokol's main entry point |
| 2 | `SOKOL_GLCORE` | Use OpenGL Core backend |
| 6 | `sokol_app.h` | Application layer |
| 7 | `sokol_gfx.h` | Graphics layer |
| 9 | `sokol_log.h` | Logging utilities |
| 10 | `sokol_glue.h` | Glue layer |

### File: `shims/sokol/sokol_linux.c`
*Configuration file - includes sokol with Linux-specific defines*

| Line | Component | Description |
|------|-----------|-------------|
| 2 | `SOKOL_IMPL` | Enable implementation |
| 3 | `dlopen` | Redirects to `cosmo_dlopen` |
| 4 | `dlsym` | Redirects to `cosmo_dlsym` |
| 10 | `sokol_app.h` | Include sokol application layer |
| 11 | `sokol_gfx.h` | Include sokol graphics layer |

### File: `shims/sokol/sokol_windows.c`
*Win32 type definitions and sokol includes*

| Line | Type/Constant | Description |
|------|--------------|-------------|
| 1-294 | Type Definitions | LARGE_INTEGER, RECT, POINT, MSG, PIXELFORMATDESCRIPTOR, etc. |
| 296 | `freopen_s` | `static errno_t freopen_s(FILE ** stream, const char * fileName, const char * mode, FILE* oldStream)` |
| 304-307 | Sokol Includes | Include sokol_windows.h, sokol_app.h, sokol_gfx.h |

### File: `shims/sokol/sokol_macos.c`
*macOS stub implementation (requires Objective-C runtime for full implementation)*

| Line | Function Name | Signature |
|------|--------------|-----------|
| 56 | `_macos_not_implemented` | `static void _macos_not_implemented(const char* func)` |
| 73 | `macos_sapp_isvalid` | `bool macos_sapp_isvalid(void)` |
| 77 | `macos_sapp_width` | `int macos_sapp_width(void)` |
| 81 | `macos_sapp_widthf` | `float macos_sapp_widthf(void)` |
| 85 | `macos_sapp_height` | `int macos_sapp_height(void)` |
| 89 | `macos_sapp_heightf` | `float macos_sapp_heightf(void)` |
| 93 | `macos_sapp_color_format` | `int macos_sapp_color_format(void)` |
| 97 | `macos_sapp_depth_format` | `int macos_sapp_depth_format(void)` |
| 101 | `macos_sapp_sample_count` | `int macos_sapp_sample_count(void)` |
| 105 | `macos_sapp_high_dpi` | `bool macos_sapp_high_dpi(void)` |
| 109 | `macos_sapp_dpi_scale` | `float macos_sapp_dpi_scale(void)` |
| 113 | `macos_sapp_show_keyboard` | `void macos_sapp_show_keyboard(bool show)` |
| 117 | `macos_sapp_keyboard_shown` | `bool macos_sapp_keyboard_shown(void)` |
| 121 | `macos_sapp_is_fullscreen` | `bool macos_sapp_is_fullscreen(void)` |
| 125 | `macos_sapp_toggle_fullscreen` | `void macos_sapp_toggle_fullscreen(void)` |
| 128 | `macos_sapp_show_mouse` | `void macos_sapp_show_mouse(bool show)` |
| 132 | `macos_sapp_mouse_shown` | `bool macos_sapp_mouse_shown(void)` |
| 136 | `macos_sapp_lock_mouse` | `void macos_sapp_lock_mouse(bool lock)` |
| 140 | `macos_sapp_mouse_locked` | `bool macos_sapp_mouse_locked(void)` |
| 144 | `macos_sapp_set_mouse_cursor` | `void macos_sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` |
| 148 | `macos_sapp_get_mouse_cursor` | `sapp_mouse_cursor macos_sapp_get_mouse_cursor(void)` |
| 152 | `macos_sapp_userdata` | `void* macos_sapp_userdata(void)` |
| 156 | `macos_sapp_query_desc` | `sapp_desc macos_sapp_query_desc(void)` |
| 160 | `macos_sapp_request_quit` | `void macos_sapp_request_quit(void)` |
| 163 | `macos_sapp_cancel_quit` | `void macos_sapp_cancel_quit(void)` |
| 166 | `macos_sapp_quit` | `void macos_sapp_quit(void)` |
| 173 | `macos_sapp_consume_event` | `void macos_sapp_consume_event(void)` |
| 176 | `macos_sapp_frame_count` | `uint64_t macos_sapp_frame_count(void)` |
| 180 | `macos_sapp_frame_duration` | `double macos_sapp_frame_duration(void)` |
| 184 | `macos_sapp_set_clipboard_string` | `void macos_sapp_set_clipboard_string(const char* str)` |
| 188 | `macos_sapp_get_clipboard_string` | `const char* macos_sapp_get_clipboard_string(void)` |
| 192 | `macos_sapp_set_window_title` | `void macos_sapp_set_window_title(const char* str)` |
| 196 | `macos_sapp_set_icon` | `void macos_sapp_set_icon(const sapp_icon_desc* icon_desc)` |
| 200 | `macos_sapp_get_num_dropped_files` | `int macos_sapp_get_num_dropped_files(void)` |
| 204 | `macos_sapp_get_dropped_file_path` | `const char* macos_sapp_get_dropped_file_path(int index)` |
| 209 | `macos_sapp_run` | `void macos_sapp_run(const sapp_desc* desc)` |
| 232 | `macos_sapp_egl_get_display` | `const void* macos_sapp_egl_get_display(void)` |
| 236 | `macos_sapp_egl_get_context` | `const void* macos_sapp_egl_get_context(void)` |
| 240 | `macos_sapp_html5_ask_leave_site` | `void macos_sapp_html5_ask_leave_site(bool ask)` |
| 244 | `macos_sapp_html5_get_dropped_file_size` | `uint32_t macos_sapp_html5_get_dropped_file_size(int index)` |
| 249 | `macos_sapp_html5_fetch_dropped_file` | `void macos_sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` |
| 253 | `macos_sapp_metal_get_device` | `const void* macos_sapp_metal_get_device(void)` |
| 257 | `macos_sapp_metal_get_current_drawable` | `const void* macos_sapp_metal_get_current_drawable(void)` |
| 261 | `macos_sapp_metal_get_depth_stencil_texture` | `const void* macos_sapp_metal_get_depth_stencil_texture(void)` |
| 265 | `macos_sapp_metal_get_msaa_color_texture` | `const void* macos_sapp_metal_get_msaa_color_texture(void)` |
| 269 | `macos_sapp_macos_get_window` | `const void* macos_sapp_macos_get_window(void)` |
| 273 | `macos_sapp_ios_get_window` | `const void* macos_sapp_ios_get_window(void)` |
| 277 | `macos_sapp_d3d11_get_device` | `const void* macos_sapp_d3d11_get_device(void)` |
| 281 | `macos_sapp_d3d11_get_device_context` | `const void* macos_sapp_d3d11_get_device_context(void)` |
| 285 | `macos_sapp_d3d11_get_swap_chain` | `const void* macos_sapp_d3d11_get_swap_chain(void)` |
| 289 | `macos_sapp_d3d11_get_render_view` | `const void* macos_sapp_d3d11_get_render_view(void)` |
| 293 | `macos_sapp_d3d11_get_resolve_view` | `const void* macos_sapp_d3d11_get_resolve_view(void)` |
| 297 | `macos_sapp_d3d11_get_depth_stencil_view` | `const void* macos_sapp_d3d11_get_depth_stencil_view(void)` |
| 301 | `macos_sapp_win32_get_hwnd` | `const void* macos_sapp_win32_get_hwnd(void)` |
| 305 | `macos_sapp_wgpu_get_device` | `const void* macos_sapp_wgpu_get_device(void)` |
| 309 | `macos_sapp_wgpu_get_render_view` | `const void* macos_sapp_wgpu_get_render_view(void)` |
| 313 | `macos_sapp_wgpu_get_resolve_view` | `const void* macos_sapp_wgpu_get_resolve_view(void)` |
| 317 | `macos_sapp_wgpu_get_depth_stencil_view` | `const void* macos_sapp_wgpu_get_depth_stencil_view(void)` |
| 321 | `macos_sapp_gl_get_framebuffer` | `uint32_t macos_sapp_gl_get_framebuffer(void)` |
| 325 | `macos_sapp_gl_get_major_version` | `int macos_sapp_gl_get_major_version(void)` |
| 329 | `macos_sapp_gl_get_minor_version` | `int macos_sapp_gl_get_minor_version(void)` |
| 333 | `macos_sapp_android_get_native_activity` | `const void* macos_sapp_android_get_native_activity(void)` |
| 341 | `macos_sg_setup` | `void macos_sg_setup(const sg_desc* desc)` |
| 349 | `macos_sg_shutdown` | `void macos_sg_shutdown(void)` |
| 353 | `macos_sg_isvalid` | `bool macos_sg_isvalid(void)` |
| 357 | `macos_sg_reset_state_cache` | `void macos_sg_reset_state_cache(void)` |
| 360 | `macos_sg_install_trace_hooks` | `sg_trace_hooks macos_sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` |
| 366 | `macos_sg_push_debug_group` | `void macos_sg_push_debug_group(const char* name)` |
| 370 | `macos_sg_pop_debug_group` | `void macos_sg_pop_debug_group(void)` |
| 373 | `macos_sg_add_commit_listener` | `bool macos_sg_add_commit_listener(sg_commit_listener listener)` |
| 378 | `macos_sg_remove_commit_listener` | `bool macos_sg_remove_commit_listener(sg_commit_listener listener)` |
| 383 | `macos_sg_make_buffer` | `sg_buffer macos_sg_make_buffer(const sg_buffer_desc* desc)` |
| 389 | `macos_sg_make_image` | `sg_image macos_sg_make_image(const sg_image_desc* desc)` |
| 395 | `macos_sg_make_sampler` | `sg_sampler macos_sg_make_sampler(const sg_sampler_desc* desc)` |
| 401 | `macos_sg_make_shader` | `sg_shader macos_sg_make_shader(const sg_shader_desc* desc)` |
| 407 | `macos_sg_make_pipeline` | `sg_pipeline macos_sg_make_pipeline(const sg_pipeline_desc* desc)` |
| 413 | `macos_sg_make_attachments` | `sg_attachments macos_sg_make_attachments(const sg_attachments_desc* desc)` |
| 419 | `macos_sg_destroy_buffer` | `void macos_sg_destroy_buffer(sg_buffer buf)` |
| 423 | `macos_sg_destroy_image` | `void macos_sg_destroy_image(sg_image img)` |
| 427 | `macos_sg_destroy_sampler` | `void macos_sg_destroy_sampler(sg_sampler smp)` |
| 431 | `macos_sg_destroy_shader` | `void macos_sg_destroy_shader(sg_shader shd)` |
| 435 | `macos_sg_destroy_pipeline` | `void macos_sg_destroy_pipeline(sg_pipeline pip)` |
| 439 | `macos_sg_destroy_attachments` | `void macos_sg_destroy_attachments(sg_attachments atts)` |
| 443 | `macos_sg_update_buffer` | `void macos_sg_update_buffer(sg_buffer buf, const sg_range* data)` |
| 448 | `macos_sg_update_image` | `void macos_sg_update_image(sg_image img, const sg_image_data* data)` |
| 453 | `macos_sg_append_buffer` | `int macos_sg_append_buffer(sg_buffer buf, const sg_range* data)` |
| 459 | `macos_sg_query_buffer_overflow` | `bool macos_sg_query_buffer_overflow(sg_buffer buf)` |
| 464 | `macos_sg_query_buffer_will_overflow` | `bool macos_sg_query_buffer_will_overflow(sg_buffer buf, size_t size)` |
| 470 | `macos_sg_begin_pass` | `void macos_sg_begin_pass(const sg_pass* pass)` |
| 474 | `macos_sg_apply_viewport` | `void macos_sg_apply_viewport(int x, int y, int width, int height, bool origin_top_left)` |
| 478 | `macos_sg_apply_viewportf` | `void macos_sg_apply_viewportf(float x, float y, float width, float height, bool origin_top_left)` |
| 482 | `macos_sg_apply_scissor_rect` | `void macos_sg_apply_scissor_rect(int x, int y, int width, int height, bool origin_top_left)` |
| 486 | `macos_sg_apply_scissor_rectf` | `void macos_sg_apply_scissor_rectf(float x, float y, float width, float height, bool origin_top_left)` |
| 490 | `macos_sg_apply_pipeline` | `void macos_sg_apply_pipeline(sg_pipeline pip)` |
| 494 | `macos_sg_apply_bindings` | `void macos_sg_apply_bindings(const sg_bindings* bindings)` |
| 498 | `macos_sg_apply_uniforms` | `void macos_sg_apply_uniforms(int ub_slot, const sg_range* data)` |
| 503 | `macos_sg_draw` | `void macos_sg_draw(int base_element, int num_elements, int num_instances)` |
| 509 | `macos_sg_end_pass` | `void macos_sg_end_pass(void)` |
| 512 | `macos_sg_commit` | `void macos_sg_commit(void)` |
| 515 | `macos_sg_query_desc` | `sg_desc macos_sg_query_desc(void)` |
| 519 | `macos_sg_query_backend` | `sg_backend macos_sg_query_backend(void)` |
| 523 | `macos_sg_query_features` | `sg_features macos_sg_query_features(void)` |
| 528 | `macos_sg_query_limits` | `sg_limits macos_sg_query_limits(void)` |
| 533 | `macos_sg_query_pixelformat` | `sg_pixelformat_info macos_sg_query_pixelformat(sg_pixel_format fmt)` |
| 539 | `macos_sg_query_row_pitch` | `int macos_sg_query_row_pitch(sg_pixel_format fmt, int width, int row_align_bytes)` |
| 544 | `macos_sg_query_surface_pitch` | `int macos_sg_query_surface_pitch(sg_pixel_format fmt, int width, int height, int row_align_bytes)` |
| 549-697 | *Additional sokol_gfx stubs* | Query functions for buffers, images, samplers, shaders, pipelines, attachments, defaults, alloc, dealloc, init, uninit, fail functions |

### File: `shims/sokol/sokol_cosmo.c`
*Runtime dispatch layer - routes sokol calls to platform-specific implementations*

**sokol_app dispatch functions (sapp_*):**

| Line | Function Name | Signature |
|------|--------------|-----------|
| 10 | `sapp_isvalid` | `bool sapp_isvalid(void)` |
| 22 | `sapp_width` | `int sapp_width(void)` |
| 34 | `sapp_widthf` | `float sapp_widthf(void)` |
| 46 | `sapp_height` | `int sapp_height(void)` |
| 58 | `sapp_heightf` | `float sapp_heightf(void)` |
| 70 | `sapp_color_format` | `int sapp_color_format(void)` |
| 82 | `sapp_depth_format` | `int sapp_depth_format(void)` |
| 94 | `sapp_sample_count` | `int sapp_sample_count(void)` |
| 106 | `sapp_high_dpi` | `bool sapp_high_dpi(void)` |
| 118 | `sapp_dpi_scale` | `float sapp_dpi_scale(void)` |
| 130 | `sapp_show_keyboard` | `void sapp_show_keyboard(bool show)` |
| 145 | `sapp_keyboard_shown` | `bool sapp_keyboard_shown(void)` |
| 157 | `sapp_is_fullscreen` | `bool sapp_is_fullscreen(void)` |
| 169 | `sapp_toggle_fullscreen` | `void sapp_toggle_fullscreen(void)` |
| 184 | `sapp_show_mouse` | `void sapp_show_mouse(bool show)` |
| 199 | `sapp_mouse_shown` | `bool sapp_mouse_shown(void)` |
| 211 | `sapp_lock_mouse` | `void sapp_lock_mouse(bool lock)` |
| 226 | `sapp_mouse_locked` | `bool sapp_mouse_locked(void)` |
| 238 | `sapp_set_mouse_cursor` | `void sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` |
| 253 | `sapp_get_mouse_cursor` | `sapp_mouse_cursor sapp_get_mouse_cursor(void)` |
| 265 | `sapp_userdata` | `void* sapp_userdata(void)` |
| 277 | `sapp_query_desc` | `sapp_desc sapp_query_desc(void)` |
| 289 | `sapp_request_quit` | `void sapp_request_quit(void)` |
| 304 | `sapp_cancel_quit` | `void sapp_cancel_quit(void)` |
| 319 | `sapp_quit` | `void sapp_quit(void)` |
| 334 | `sapp_consume_event` | `void sapp_consume_event(void)` |
| 349 | `sapp_frame_count` | `uint64_t sapp_frame_count(void)` |
| 361 | `sapp_frame_duration` | `double sapp_frame_duration(void)` |
| 373 | `sapp_set_clipboard_string` | `void sapp_set_clipboard_string(const char* str)` |
| 388 | `sapp_get_clipboard_string` | `const char* sapp_get_clipboard_string(void)` |
| 400 | `sapp_set_window_title` | `void sapp_set_window_title(const char* str)` |
| 415 | `sapp_set_icon` | `void sapp_set_icon(const sapp_icon_desc* icon_desc)` |
| 430 | `sapp_get_num_dropped_files` | `int sapp_get_num_dropped_files(void)` |
| 442 | `sapp_get_dropped_file_path` | `const char* sapp_get_dropped_file_path(int index)` |
| 454 | `sapp_run` | `void sapp_run(const sapp_desc* desc)` |
| 469 | `sapp_egl_get_display` | `const void* sapp_egl_get_display(void)` |
| 481 | `sapp_egl_get_context` | `const void* sapp_egl_get_context(void)` |
| 493 | `sapp_html5_ask_leave_site` | `void sapp_html5_ask_leave_site(bool ask)` |
| 508 | `sapp_html5_get_dropped_file_size` | `uint32_t sapp_html5_get_dropped_file_size(int index)` |
| 520 | `sapp_html5_fetch_dropped_file` | `void sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` |
| 535 | `sapp_metal_get_device` | `const void* sapp_metal_get_device(void)` |
| 547 | `sapp_metal_get_current_drawable` | `const void* sapp_metal_get_current_drawable(void)` |
| 559 | `sapp_metal_get_depth_stencil_texture` | `const void* sapp_metal_get_depth_stencil_texture(void)` |
| 571 | `sapp_metal_get_msaa_color_texture` | `const void* sapp_metal_get_msaa_color_texture(void)` |
| 583 | `sapp_macos_get_window` | `const void* sapp_macos_get_window(void)` |
| 595 | `sapp_ios_get_window` | `const void* sapp_ios_get_window(void)` |
| 607 | `sapp_d3d11_get_device` | `const void* sapp_d3d11_get_device(void)` |
| 619 | `sapp_d3d11_get_device_context` | `const void* sapp_d3d11_get_device_context(void)` |
| 631 | `sapp_d3d11_get_swap_chain` | `const void* sapp_d3d11_get_swap_chain(void)` |
| 643 | `sapp_d3d11_get_render_view` | `const void* sapp_d3d11_get_render_view(void)` |
| 655 | `sapp_d3d11_get_resolve_view` | `const void* sapp_d3d11_get_resolve_view(void)` |
| 667 | `sapp_d3d11_get_depth_stencil_view` | `const void* sapp_d3d11_get_depth_stencil_view(void)` |
| 679 | `sapp_win32_get_hwnd` | `const void* sapp_win32_get_hwnd(void)` |
| 691 | `sapp_wgpu_get_device` | `const void* sapp_wgpu_get_device(void)` |
| 703 | `sapp_wgpu_get_render_view` | `const void* sapp_wgpu_get_render_view(void)` |
| 715 | `sapp_wgpu_get_resolve_view` | `const void* sapp_wgpu_get_resolve_view(void)` |
| 727 | `sapp_wgpu_get_depth_stencil_view` | `const void* sapp_wgpu_get_depth_stencil_view(void)` |
| 739 | `sapp_gl_get_framebuffer` | `uint32_t sapp_gl_get_framebuffer(void)` |
| 751 | `sapp_gl_get_major_version` | `int sapp_gl_get_major_version(void)` |
| 763 | `sapp_gl_get_minor_version` | `int sapp_gl_get_minor_version(void)` |
| 775 | `sapp_android_get_native_activity` | `const void* sapp_android_get_native_activity(void)` |

**sokol_gfx dispatch functions (sg_*):**

| Line | Function Name | Signature |
|------|--------------|-----------|
| 787 | `sg_setup` | `void sg_setup(const sg_desc* desc)` |
| 802 | `sg_shutdown` | `void sg_shutdown(void)` |
| 817 | `sg_isvalid` | `bool sg_isvalid(void)` |
| 829 | `sg_reset_state_cache` | `void sg_reset_state_cache(void)` |
| 844 | `sg_install_trace_hooks` | `sg_trace_hooks sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` |
| 856 | `sg_push_debug_group` | `void sg_push_debug_group(const char* name)` |
| 871 | `sg_pop_debug_group` | `void sg_pop_debug_group(void)` |
| 886 | `sg_add_commit_listener` | `bool sg_add_commit_listener(sg_commit_listener listener)` |
| 898 | `sg_remove_commit_listener` | `bool sg_remove_commit_listener(sg_commit_listener listener)` |
| 910 | `sg_make_buffer` | `sg_buffer sg_make_buffer(const sg_buffer_desc* desc)` |
| 922 | `sg_make_image` | `sg_image sg_make_image(const sg_image_desc* desc)` |
| 934 | `sg_make_sampler` | `sg_sampler sg_make_sampler(const sg_sampler_desc* desc)` |
| 946 | `sg_make_shader` | `sg_shader sg_make_shader(const sg_shader_desc* desc)` |
| 958 | `sg_make_pipeline` | `sg_pipeline sg_make_pipeline(const sg_pipeline_desc* desc)` |
| 970 | `sg_make_attachments` | `sg_attachments sg_make_attachments(const sg_attachments_desc* desc)` |
| 982 | `sg_destroy_buffer` | `void sg_destroy_buffer(sg_buffer buf)` |
| 997 | `sg_destroy_image` | `void sg_destroy_image(sg_image img)` |
| 1012 | `sg_destroy_sampler` | `void sg_destroy_sampler(sg_sampler smp)` |
| 1027 | `sg_destroy_shader` | `void sg_destroy_shader(sg_shader shd)` |
| 1042 | `sg_destroy_pipeline` | `void sg_destroy_pipeline(sg_pipeline pip)` |
| 1057 | `sg_destroy_attachments` | `void sg_destroy_attachments(sg_attachments atts)` |
| 1072 | `sg_update_buffer` | `void sg_update_buffer(sg_buffer buf, const sg_range* data)` |
| 1087 | `sg_update_image` | `void sg_update_image(sg_image img, const sg_image_data* data)` |
| 1102 | `sg_append_buffer` | `int sg_append_buffer(sg_buffer buf, const sg_range* data)` |
| 1114 | `sg_query_buffer_overflow` | `bool sg_query_buffer_overflow(sg_buffer buf)` |
| 1126 | `sg_query_buffer_will_overflow` | `bool sg_query_buffer_will_overflow(sg_buffer buf, size_t size)` |
| 1138 | `sg_begin_pass` | `void sg_begin_pass(const sg_pass* pass)` |
| 1153 | `sg_apply_viewport` | `void sg_apply_viewport(int x, int y, int width, int height, bool origin_top_left)` |
| 1168 | `sg_apply_viewportf` | `void sg_apply_viewportf(float x, float y, float width, float height, bool origin_top_left)` |
| 1183 | `sg_apply_scissor_rect` | `void sg_apply_scissor_rect(int x, int y, int width, int height, bool origin_top_left)` |
| 1198 | `sg_apply_scissor_rectf` | `void sg_apply_scissor_rectf(float x, float y, float width, float height, bool origin_top_left)` |
| 1213 | `sg_apply_pipeline` | `void sg_apply_pipeline(sg_pipeline pip)` |
| 1228 | `sg_apply_bindings` | `void sg_apply_bindings(const sg_bindings* bindings)` |
| 1243 | `sg_apply_uniforms` | `void sg_apply_uniforms(int ub_slot, const sg_range* data)` |
| 1258 | `sg_draw` | `void sg_draw(int base_element, int num_elements, int num_instances)` |
| 1273 | `sg_end_pass` | `void sg_end_pass(void)` |
| 1288 | `sg_commit` | `void sg_commit(void)` |
| 1303 | `sg_query_desc` | `sg_desc sg_query_desc(void)` |
| 1315 | `sg_query_backend` | `sg_backend sg_query_backend(void)` |
| 1327 | `sg_query_features` | `sg_features sg_query_features(void)` |
| 1339 | `sg_query_limits` | `sg_limits sg_query_limits(void)` |
| 1351 | `sg_query_pixelformat` | `sg_pixelformat_info sg_query_pixelformat(sg_pixel_format fmt)` |
| 1363 | `sg_query_row_pitch` | `int sg_query_row_pitch(sg_pixel_format fmt, int width, int row_align_bytes)` |
| 1375 | `sg_query_surface_pitch` | `int sg_query_surface_pitch(sg_pixel_format fmt, int width, int height, int row_align_bytes)` |
| 1387-3099 | *Additional dispatch functions* | Buffer/image/sampler/shader/pipeline/attachments state, info, desc, defaults, alloc, dealloc, init, uninit, fail, frame stats, D3D11, Metal, WGPU, OpenGL backend queries |

### File: `shims/linux/x11.c`
*X11 library dynamic loading shim*

**Internal loader functions:**

| Line | Function Name | Signature |
|------|--------------|-----------|
| 85 | `load_X11_procs` | `static void load_X11_procs(void)` |
| 193 | `load_Xcursor_procs` | `static void load_Xcursor_procs(void)` |
| 208 | `load_Xi_procs` | `static void load_Xi_procs(void)` |

**X11 wrapper functions:**

| Line | Function Name | Signature |
|------|--------------|-----------|
| 217 | `XOpenDisplay` | `Display * XOpenDisplay(const char* display_name)` |
| 223 | `XCloseDisplay` | `int XCloseDisplay(Display* display)` |
| 229 | `XFlush` | `int XFlush(Display* display)` |
| 235 | `XNextEvent` | `int XNextEvent(Display* display, XEvent* event_return)` |
| 241 | `XPending` | `int XPending(Display* display)` |
| 247 | `XInitThreads` | `Status XInitThreads(void)` |
| 253 | `XFilterEvent` | `Bool XFilterEvent(XEvent* event, Window w)` |
| 259 | `XkbSetDetectableAutoRepeat` | `Bool XkbSetDetectableAutoRepeat(Display* display, Bool detectable, Bool* supported_rtrn)` |
| 265 | `XSync` | `int XSync(Display* display, Bool discard)` |
| 271 | `XrmInitialize` | `void XrmInitialize(void)` |
| 277 | `XChangeProperty` | `int XChangeProperty(Display* display, Window w, Atom property, Atom type, int format, int mode, const unsigned char* data, int nelements)` |
| 283 | `XSendEvent` | `Status XSendEvent(Display* display, Window w, Bool propagate, long event_mask, XEvent* event_send)` |
| 289 | `XFree` | `int XFree(void* data)` |
| 295 | `XSetErrorHandler` | `XErrorHandler XSetErrorHandler(XErrorHandler handler)` |
| 301 | `XConvertSelection` | `int XConvertSelection(Display* display, Atom selection, Atom target, Atom property, Window requestor, Time time)` |
| 307 | `XLookupString` | `int XLookupString(XKeyEvent* event_struct, char* buffer_return, int bytes_buffer, KeySym* keysym_return, XComposeStatus* status_in_out)` |
| 313 | `XGetEventData` | `Bool XGetEventData(Display* display, XGenericEventCookie* cookie)` |
| 319 | `XFreeEventData` | `void XFreeEventData(Display* display, XGenericEventCookie* cookie)` |
| 325 | `XGetWindowProperty` | `int XGetWindowProperty(Display* display, Window w, Atom property, long long_offset, long long_length, Bool delete, Atom req_type, Atom* actual_type_return, int* actual_format_return, unsigned long* nitems_return, unsigned long* bytes_after_return, unsigned char** prop_return)` |
| 331 | `XMapWindow` | `int XMapWindow(Display* display, Window w)` |
| 337 | `XUnmapWindow` | `int XUnmapWindow(Display* display, Window w)` |
| 343 | `XRaiseWindow` | `int XRaiseWindow(Display* display, Window w)` |
| 349 | `XGetWindowAttributes` | `Status XGetWindowAttributes(Display* display, Window w, XWindowAttributes* window_attributes_return)` |
| 355 | `XAllocSizeHints` | `XSizeHints * XAllocSizeHints(void)` |
| 361 | `XCheckTypedWindowEvent` | `Bool XCheckTypedWindowEvent(Display* display, Window w, int event_type, XEvent* event_return)` |
| 367 | `XCreateColormap` | `Colormap XCreateColormap(Display* display, Window w, Visual* visual, int alloc)` |
| 373 | `XCreateFontCursor` | `Cursor XCreateFontCursor(Display* display, unsigned int shape)` |
| 379 | `XCreateWindow` | `Window XCreateWindow(Display* display, Window parent, int x, int y, unsigned int width, unsigned int height, unsigned int border_width, int depth, unsigned int class, Visual* visual, unsigned long valuemask, XSetWindowAttributes* attributes)` |
| 385 | `XWarpPointer` | `int XWarpPointer(Display* display, Window src_w, Window dest_w, int src_x, int src_y, unsigned int src_width, unsigned int src_height, int dest_x, int dest_y)` |
| 391 | `XDefineCursor` | `int XDefineCursor(Display* display, Window w, Cursor cursor)` |
| 397 | `XDestroyWindow` | `int XDestroyWindow(Display* display, Window w)` |
| 403 | `XFreeColormap` | `int XFreeColormap(Display* display, Colormap colormap)` |
| 409 | `XFreeCursor` | `int XFreeCursor(Display* display, Cursor cursor)` |
| 415 | `XGetKeyboardMapping` | `KeySym * XGetKeyboardMapping(Display* display, unsigned int first_keycode, int keycode_count, int* keysyms_per_keycode_return)` |
| 421 | `XGetSelectionOwner` | `Window XGetSelectionOwner(Display* display, Atom selection)` |
| 427 | `XGrabPointer` | `int XGrabPointer(Display* display, Window grab_window, Bool owner_events, unsigned int event_mask, int pointer_mode, int keyboard_mode, Window confine_to, Cursor cursor, Time time)` |
| 433 | `XInternAtom` | `Atom XInternAtom(Display* display, const char* atom_name, Bool only_if_exists)` |
| 439 | `XInternAtoms` | `Status XInternAtoms(Display* display, char** names, int count, Bool only_if_exists, Atom* atoms_return)` |
| 445 | `XSetSelectionOwner` | `int XSetSelectionOwner(Display* display, Atom selection, Window owner, Time time)` |
| 451 | `XSetWMNormalHints` | `void XSetWMNormalHints(Display* display, Window w, XSizeHints* hints)` |
| 457 | `XSetWMProtocols` | `Status XSetWMProtocols(Display* display, Window w, Atom* protocols, int count)` |
| 463 | `XUndefineCursor` | `int XUndefineCursor(Display* display, Window w)` |
| 469 | `XUngrabPointer` | `int XUngrabPointer(Display* display, Time time)` |
| 475 | `Xutf8SetWMProperties` | `void Xutf8SetWMProperties(Display* display, Window w, const char* window_name, const char* icon_name, char** argv, int argc, XSizeHints* normal_hints, XWMHints* wm_hints, XClassHint* class_hints)` |
| 481 | `XkbFreeKeyboard` | `void XkbFreeKeyboard(XkbDescPtr xkb, unsigned int which, Bool free_all)` |
| 487 | `XkbFreeNames` | `void XkbFreeNames(XkbDescPtr xkb, unsigned int which, Bool free_map)` |
| 493 | `XResourceManagerString` | `char * XResourceManagerString(Display* display)` |
| 499 | `XrmDestroyDatabase` | `void XrmDestroyDatabase(XrmDatabase database)` |
| 505 | `XrmGetResource` | `Bool XrmGetResource(XrmDatabase database, const char* str_name, const char* str_class, char** str_type_return, XrmValue* value_return)` |
| 511 | `XkbGetMap` | `XkbDescPtr XkbGetMap(Display* display, unsigned int which, unsigned int device_spec)` |
| 517 | `XkbGetNames` | `Status XkbGetNames(Display* dpy, unsigned int which, XkbDescPtr xkb)` |
| 523 | `XrmGetStringDatabase` | `XrmDatabase XrmGetStringDatabase(const char* data)` |
| 529 | `XQueryExtension` | `Bool XQueryExtension(Display* display, const char* name, int* major_opcode_return, int* first_event_return, int* first_error_return)` |
| 535 | `XcursorGetDefaultSize` | `int XcursorGetDefaultSize(Display* dpy)` |
| 541 | `XcursorGetTheme` | `char * XcursorGetTheme(Display* dpy)` |
| 547 | `XcursorImageCreate` | `XcursorImage * XcursorImageCreate(int width, int height)` |
| 553 | `XcursorImageDestroy` | `void XcursorImageDestroy(XcursorImage* image)` |
| 559 | `XcursorImageLoadCursor` | `Cursor XcursorImageLoadCursor(Display* dpy, const XcursorImage* image)` |
| 565 | `XcursorLibraryLoadImage` | `XcursorImage * XcursorLibraryLoadImage(const char* library, const char* theme, int size)` |
| 571 | `XIQueryVersion` | `Status XIQueryVersion(Display* dpy, int* major_version_inout, int* minor_version_inout)` |
| 577 | `XISelectEvents` | `int XISelectEvents(Display* dpy, Window win, XIEventMask* masks, int num_masks)` |

### File: `shims/linux/gl.c`
*OpenGL library dynamic loading shim (~6000+ lines)*

**Summary:** Contains 500+ OpenGL function wrappers that load from `libGL.so` at runtime via `cosmo_dlopen`/`cosmo_dlsym`.

Key wrapper pattern (first ~100 functions):

| Line | Function Name | Return Type |
|------|--------------|-------------|
| 7 | `glAccum` | `void` |
| 8 | `glActiveTexture` | `void` |
| 9 | `glAlphaFunc` | `void` |
| 10 | `glAreTexturesResident` | `GLboolean` |
| 11 | `glArrayElement` | `void` |
| 12 | `glAttachShader` | `void` |
| 13 | `glBegin` | `void` |
| ... | ... | ... |

*See full file for complete list of 500+ GL functions.*

---

## CI/CD Workflow Analysis

### Current Workflow: `.github/workflows/build.yml`

```yaml
name: Build
on: [push]
permissions:
  contents: write
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - checkout with submodules: recursive
      - Install deps (libx11-dev, libgl-dev, libxcursor-dev, libxi-dev)
      - Download cosmocc 3.9.6 via bjia56/setup-cosmocc
      - Build via ./build script
      - Package binaries (on tags)
      - Release draft (on tags via softprops/action-gh-release)
```

### Concurrency Control
```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```
✅ Good: Prevents redundant builds on rapid pushes.

---

## CI/CD Recommendations

### 1. Add Upstream Sync Workflow

**Priority: HIGH**

Create `.github/workflows/sync-upstream.yml`:

```yaml
name: Sync Upstream
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly on Mondays
  workflow_dispatch:

jobs:
  sync-sokol:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
      
      - name: Sync floooh/sokol
        run: |
          cd deps/sokol
          git fetch origin
          LATEST=$(git describe --tags $(git rev-list --tags --max-count=1) 2>/dev/null || git rev-parse origin/master)
          git checkout $LATEST
          cd ../..
          git add deps/sokol
          if git diff --cached --quiet; then
            echo "Already up to date"
          else
            git commit -m "deps: update sokol to $LATEST"
            git push
          fi

  sync-cimgui:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
          fetch-depth: 0
      
      - name: Sync cimgui
        run: |
          cd deps/cimgui
          git fetch origin
          LATEST=$(git describe --tags $(git rev-list --tags --max-count=1) 2>/dev/null || git rev-parse origin/master)
          git checkout $LATEST
          cd ../..
          git add deps/cimgui
          if git diff --cached --quiet; then
            echo "Already up to date"
          else
            git commit -m "deps: update cimgui to $LATEST"
            git push
          fi
```

### 2. Add Cross-Platform Testing

**Priority: MEDIUM**

The binary is cross-platform APE, but we should at least test on multiple OS runners:

```yaml
# Add to build.yml
jobs:
  build:
    runs-on: ubuntu-latest
    # ... existing steps ...

  test-linux:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - name: Test binary loads
        run: |
          chmod +x bin/cosmo-sokol
          timeout 5 ./bin/cosmo-sokol --help || [ $? -eq 124 ]

  test-macos:
    needs: build
    runs-on: macos-latest
    steps:
      - uses: actions/download-artifact@v4
      - name: Test binary loads
        run: |
          chmod +x bin/cosmo-sokol
          # Note: Will fail on macOS until stub is implemented
          ./bin/cosmo-sokol --help 2>&1 | grep -q "macOS support is not yet fully implemented" && echo "Expected stub message"
```

### 3. Add Build Matrix for Cosmopolitan Versions

**Priority: LOW**

Test against multiple cosmocc versions for compatibility:

```yaml
strategy:
  matrix:
    cosmocc: ['3.9.6', '3.9.5', '3.8.0']
steps:
  - uses: bjia56/setup-cosmocc@main
    with:
      version: ${{ matrix.cosmocc }}
```

### 4. Add Release Changelog Generation

**Priority: MEDIUM**

```yaml
- name: Generate Changelog
  if: startsWith(github.ref, 'refs/tags/')
  run: |
    PREV_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
    if [ -n "$PREV_TAG" ]; then
      git log --pretty=format:"- %s" $PREV_TAG..HEAD > CHANGELOG.md
    else
      echo "Initial release" > CHANGELOG.md
    fi

- name: Release
  uses: softprops/action-gh-release@v2
  with:
    body_path: CHANGELOG.md
    files: bin/cosmo-sokol.zip
```

### 5. Create C-Based Smoke Test (Philosophy-Compliant)

**Priority: HIGH**

Create `tests/smoke.c` — a simple C program that validates the build:

```c
// tests/smoke.c - Cosmopolitan smoke test (NO interpreters!)
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    printf("SMOKE TEST: cosmo-sokol build validation\n");
    
    // Test 1: Verify we're running on expected platform
    #ifdef __COSMOPOLITAN__
    printf("✓ Cosmopolitan APE detected\n");
    #else
    printf("✗ Not a Cosmopolitan binary\n");
    return 1;
    #endif
    
    // Test 2: Verify sokol types exist
    // (Would include sokol headers and check types)
    
    printf("SMOKE TEST: PASSED\n");
    return 0;
}
```

Add to `build` script:
```sh
# Build and run smoke test
compile tests/smoke.c ${FLAGS}
cosmoc++ ${FLAGS} -o bin/smoke-test .build/tests/smoke.c.o
./bin/smoke-test
```

---

## Function Count Summary

| File | Function Count | Category |
|------|---------------|----------|
| `main.c` | 5 | Application |
| `win32_tweaks.c` | 1 | Platform/Windows |
| `nvapi/nvapi.c` | 1 | Platform/Windows |
| `shims/sokol/sokol_macos.c` | ~95 | Platform/macOS (stubs) |
| `shims/sokol/sokol_cosmo.c` | ~130 | Runtime Dispatch |
| `shims/linux/x11.c` | ~65 | Platform/Linux |
| `shims/linux/gl.c` | ~500+ | Platform/Linux (OpenGL) |
| **TOTAL** | **~800+** | |

---

## Upstream Dependencies

| Dependency | Source | Current Version | Sync Strategy |
|------------|--------|-----------------|---------------|
| sokol | floooh/sokol | submodule | Weekly automated sync |
| cimgui | cimgui/cimgui | submodule | Weekly automated sync |
| cosmopolitan | jart/cosmopolitan | cosmocc 3.9.6 | Track releases |

---

## Architecture Notes

### Runtime Dispatch Pattern

The project uses a compile-time multi-platform pattern:

1. **Platform backends** (`sokol_linux.c`, `sokol_windows.c`, `sokol_macos.c`) compile sokol with platform-specific `#define`s and prefix functions (e.g., `linux_sapp_run`, `windows_sapp_run`)

2. **Dispatch layer** (`sokol_cosmo.c`) exports the standard sokol API (`sapp_run`, `sg_setup`, etc.) and routes to platform implementations at runtime using Cosmopolitan's `IsLinux()`, `IsWindows()`, `IsXnu()` checks

3. **Shim libraries** (`shims/linux/x11.c`, `shims/linux/gl.c`) provide dynamic loading of system libraries via `cosmo_dlopen` on Linux

### Build Artifact

Single output: `bin/cosmo-sokol` — an Actually Portable Executable (APE) that runs on:
- Linux (x86-64, aarch64)
- Windows (x86-64)
- macOS (x86-64, aarch64) — *stub only*
- FreeBSD, NetBSD, OpenBSD

---

## Recommended Next Steps

1. **Implement upstream sync workflow** — Critical for staying current
2. **Add C-based smoke test** — Validate builds without interpreters
3. **Consider macOS implementation** — Currently just stubs; options:
   - Objective-C runtime via C (`objc_msgSend`)
   - Native helper dylib loaded at runtime
   - SDL/GLFW as alternative windowing layer
4. **Add artifact upload** — Currently only packages on tags; consider uploading artifacts for all builds

---

*Report generated by CI/CD agent for Swiss Rounds v4*
