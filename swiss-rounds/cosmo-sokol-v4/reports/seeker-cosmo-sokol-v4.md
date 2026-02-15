# cosmo-sokol Source Manifest

**Generated:** 2026-02-09  
**Specialist:** seeker (Source Discovery & Upstream Tracking)  
**Project:** ludoplex/cosmo-sokol  
**Upstreams:** floooh/sokol, jart/cosmopolitan

---

## Executive Summary

The cosmo-sokol project is a **Cosmopolitan-compatible fork** of the sokol header-only libraries. It achieves cross-platform portability via:

1. **Runtime Platform Dispatch** - `sokol_cosmo.c` routes all sokol calls to platform-specific implementations (linux/windows/macos prefixed functions)
2. **Symbol Renaming Macros** - Platform headers (`sokol_linux.h`, `sokol_windows.h`, `sokol_macos.h`) rename all public functions
3. **Dynamic Library Shims** - X11/GL functions loaded at runtime via `cosmo_dlopen()` for Linux compatibility
4. **Win32 Compatibility Layer** - Custom `windowsesque.h` based types and missing Win32 definitions

**File Count:** 110+ C/H files  
**Public API Functions:** 300+ across all sokol modules  
**Fork-Specific Functions:** 15 custom functions

---

## Source Tree Structure

```
C:\cosmo-sokol\
├── main.c                           # Main demo application
├── win32_tweaks.c/h                 # Windows console hiding
├── nvapi/                           # NVIDIA driver optimization
│   ├── nvapi.c
│   ├── nvapi.h
│   └── nvapi_decl.h
├── shims/
│   ├── linux/
│   │   ├── gl.c                     # OpenGL function shims (dlopen)
│   │   └── x11.c                    # X11/Xcursor/Xi shims (dlopen)
│   ├── sokol/
│   │   ├── sokol_cosmo.c            # Runtime dispatch layer
│   │   ├── sokol_linux.c/h          # Linux platform build
│   │   ├── sokol_windows.c/h        # Windows platform build
│   │   ├── sokol_macos.c/h          # macOS stubs (not yet implemented)
│   │   └── sokol_shared.c           # Shared implementation
│   └── win32/
│       ├── shellapi.h
│       └── windowsx.h
├── deps/
│   ├── sokol/                       # floooh/sokol upstream
│   │   ├── sokol_app.h
│   │   ├── sokol_gfx.h
│   │   ├── sokol_audio.h
│   │   ├── sokol_time.h
│   │   ├── sokol_fetch.h
│   │   ├── sokol_args.h
│   │   ├── sokol_log.h
│   │   ├── sokol_glue.h
│   │   └── util/
│   │       ├── sokol_gl.h
│   │       ├── sokol_debugtext.h
│   │       ├── sokol_shape.h
│   │       ├── sokol_color.h
│   │       └── ... (imgui, nuklear, etc.)
│   └── cimgui/                      # Dear ImGui C bindings
```

---

## FUNCTION MANIFEST: Upstream Sokol Headers

### sokol_gfx.h (Graphics API)
**File:** `C:\cosmo-sokol\deps\sokol\sokol_gfx.h`

| Function | Signature | Line |
|----------|-----------|------|
| sg_setup | `void sg_setup(const sg_desc* desc)` | 4174 |
| sg_shutdown | `void sg_shutdown(void)` | 4175 |
| sg_isvalid | `bool sg_isvalid(void)` | 4176 |
| sg_reset_state_cache | `void sg_reset_state_cache(void)` | 4177 |
| sg_install_trace_hooks | `sg_trace_hooks sg_install_trace_hooks(const sg_trace_hooks* trace_hooks)` | 4178 |
| sg_push_debug_group | `void sg_push_debug_group(const char* name)` | 4179 |
| sg_pop_debug_group | `void sg_pop_debug_group(void)` | 4180 |
| sg_add_commit_listener | `bool sg_add_commit_listener(sg_commit_listener listener)` | 4181 |
| sg_remove_commit_listener | `bool sg_remove_commit_listener(sg_commit_listener listener)` | 4182 |
| sg_make_buffer | `sg_buffer sg_make_buffer(const sg_buffer_desc* desc)` | 4185 |
| sg_make_image | `sg_image sg_make_image(const sg_image_desc* desc)` | 4186 |
| sg_make_sampler | `sg_sampler sg_make_sampler(const sg_sampler_desc* desc)` | 4187 |
| sg_make_shader | `sg_shader sg_make_shader(const sg_shader_desc* desc)` | 4188 |
| sg_make_pipeline | `sg_pipeline sg_make_pipeline(const sg_pipeline_desc* desc)` | 4189 |
| sg_make_attachments | `sg_attachments sg_make_attachments(const sg_attachments_desc* desc)` | 4190 |
| sg_destroy_buffer | `void sg_destroy_buffer(sg_buffer buf)` | 4191 |
| sg_destroy_image | `void sg_destroy_image(sg_image img)` | 4192 |
| sg_destroy_sampler | `void sg_destroy_sampler(sg_sampler smp)` | 4193 |
| sg_destroy_shader | `void sg_destroy_shader(sg_shader shd)` | 4194 |
| sg_destroy_pipeline | `void sg_destroy_pipeline(sg_pipeline pip)` | 4195 |
| sg_destroy_attachments | `void sg_destroy_attachments(sg_attachments atts)` | 4196 |
| sg_update_buffer | `void sg_update_buffer(sg_buffer buf, const sg_range* data)` | 4197 |
| sg_update_image | `void sg_update_image(sg_image img, const sg_image_data* data)` | 4198 |
| sg_append_buffer | `int sg_append_buffer(sg_buffer buf, const sg_range* data)` | 4199 |
| sg_query_buffer_overflow | `bool sg_query_buffer_overflow(sg_buffer buf)` | 4200 |
| sg_query_buffer_will_overflow | `bool sg_query_buffer_will_overflow(sg_buffer buf, size_t size)` | 4201 |
| sg_begin_pass | `void sg_begin_pass(const sg_pass* pass)` | 4204 |
| sg_apply_viewport | `void sg_apply_viewport(int x, int y, int width, int height, bool origin_top_left)` | 4205 |
| sg_apply_viewportf | `void sg_apply_viewportf(float x, float y, float width, float height, bool origin_top_left)` | 4206 |
| sg_apply_scissor_rect | `void sg_apply_scissor_rect(int x, int y, int width, int height, bool origin_top_left)` | 4207 |
| sg_apply_scissor_rectf | `void sg_apply_scissor_rectf(float x, float y, float width, float height, bool origin_top_left)` | 4208 |
| sg_apply_pipeline | `void sg_apply_pipeline(sg_pipeline pip)` | 4209 |
| sg_apply_bindings | `void sg_apply_bindings(const sg_bindings* bindings)` | 4210 |
| sg_apply_uniforms | `void sg_apply_uniforms(int ub_slot, const sg_range* data)` | 4211 |
| sg_draw | `void sg_draw(int base_element, int num_elements, int num_instances)` | 4212 |
| sg_end_pass | `void sg_end_pass(void)` | 4213 |
| sg_commit | `void sg_commit(void)` | 4214 |
| sg_query_desc | `sg_desc sg_query_desc(void)` | 4217 |
| sg_query_backend | `sg_backend sg_query_backend(void)` | 4218 |
| sg_query_features | `sg_features sg_query_features(void)` | 4219 |
| sg_query_limits | `sg_limits sg_query_limits(void)` | 4220 |
| sg_query_pixelformat | `sg_pixelformat_info sg_query_pixelformat(sg_pixel_format fmt)` | 4221 |
| sg_query_row_pitch | `int sg_query_row_pitch(sg_pixel_format fmt, int width, int row_align_bytes)` | 4222 |
| sg_query_surface_pitch | `int sg_query_surface_pitch(sg_pixel_format fmt, int width, int height, int row_align_bytes)` | 4223 |
| sg_query_buffer_state | `sg_resource_state sg_query_buffer_state(sg_buffer buf)` | 4225 |
| sg_query_image_state | `sg_resource_state sg_query_image_state(sg_image img)` | 4226 |
| sg_query_sampler_state | `sg_resource_state sg_query_sampler_state(sg_sampler smp)` | 4227 |
| sg_query_shader_state | `sg_resource_state sg_query_shader_state(sg_shader shd)` | 4228 |
| sg_query_pipeline_state | `sg_resource_state sg_query_pipeline_state(sg_pipeline pip)` | 4229 |
| sg_query_attachments_state | `sg_resource_state sg_query_attachments_state(sg_attachments atts)` | 4230 |
| sg_query_buffer_info | `sg_buffer_info sg_query_buffer_info(sg_buffer buf)` | 4232 |
| sg_query_image_info | `sg_image_info sg_query_image_info(sg_image img)` | 4233 |
| sg_query_sampler_info | `sg_sampler_info sg_query_sampler_info(sg_sampler smp)` | 4234 |
| sg_query_shader_info | `sg_shader_info sg_query_shader_info(sg_shader shd)` | 4235 |
| sg_query_pipeline_info | `sg_pipeline_info sg_query_pipeline_info(sg_pipeline pip)` | 4236 |
| sg_query_attachments_info | `sg_attachments_info sg_query_attachments_info(sg_attachments atts)` | 4237 |
| sg_query_buffer_desc | `sg_buffer_desc sg_query_buffer_desc(sg_buffer buf)` | 4239 |
| sg_query_image_desc | `sg_image_desc sg_query_image_desc(sg_image img)` | 4240 |
| sg_query_sampler_desc | `sg_sampler_desc sg_query_sampler_desc(sg_sampler smp)` | 4241 |
| sg_query_shader_desc | `sg_shader_desc sg_query_shader_desc(sg_shader shd)` | 4242 |
| sg_query_pipeline_desc | `sg_pipeline_desc sg_query_pipeline_desc(sg_pipeline pip)` | 4243 |
| sg_query_attachments_desc | `sg_attachments_desc sg_query_attachments_desc(sg_attachments atts)` | 4244 |
| sg_query_buffer_defaults | `sg_buffer_desc sg_query_buffer_defaults(const sg_buffer_desc* desc)` | 4246 |
| sg_query_image_defaults | `sg_image_desc sg_query_image_defaults(const sg_image_desc* desc)` | 4247 |
| sg_query_sampler_defaults | `sg_sampler_desc sg_query_sampler_defaults(const sg_sampler_desc* desc)` | 4248 |
| sg_query_shader_defaults | `sg_shader_desc sg_query_shader_defaults(const sg_shader_desc* desc)` | 4249 |
| sg_query_pipeline_defaults | `sg_pipeline_desc sg_query_pipeline_defaults(const sg_pipeline_desc* desc)` | 4250 |
| sg_query_attachments_defaults | `sg_attachments_desc sg_query_attachments_defaults(const sg_attachments_desc* desc)` | 4251 |
| sg_alloc_buffer | `sg_buffer sg_alloc_buffer(void)` | 4254 |
| sg_alloc_image | `sg_image sg_alloc_image(void)` | 4255 |
| sg_alloc_sampler | `sg_sampler sg_alloc_sampler(void)` | 4256 |
| sg_alloc_shader | `sg_shader sg_alloc_shader(void)` | 4257 |
| sg_alloc_pipeline | `sg_pipeline sg_alloc_pipeline(void)` | 4258 |
| sg_alloc_attachments | `sg_attachments sg_alloc_attachments(void)` | 4259 |
| sg_dealloc_buffer | `void sg_dealloc_buffer(sg_buffer buf)` | 4260 |
| sg_dealloc_image | `void sg_dealloc_image(sg_image img)` | 4261 |
| sg_dealloc_sampler | `void sg_dealloc_sampler(sg_sampler smp)` | 4262 |
| sg_dealloc_shader | `void sg_dealloc_shader(sg_shader shd)` | 4263 |
| sg_dealloc_pipeline | `void sg_dealloc_pipeline(sg_pipeline pip)` | 4264 |
| sg_dealloc_attachments | `void sg_dealloc_attachments(sg_attachments attachments)` | 4265 |
| sg_init_buffer | `void sg_init_buffer(sg_buffer buf, const sg_buffer_desc* desc)` | 4266 |
| sg_init_image | `void sg_init_image(sg_image img, const sg_image_desc* desc)` | 4267 |
| sg_init_sampler | `void sg_init_sampler(sg_sampler smg, const sg_sampler_desc* desc)` | 4268 |
| sg_init_shader | `void sg_init_shader(sg_shader shd, const sg_shader_desc* desc)` | 4269 |
| sg_init_pipeline | `void sg_init_pipeline(sg_pipeline pip, const sg_pipeline_desc* desc)` | 4270 |
| sg_init_attachments | `void sg_init_attachments(sg_attachments attachments, const sg_attachments_desc* desc)` | 4271 |
| sg_uninit_buffer | `void sg_uninit_buffer(sg_buffer buf)` | 4272 |
| sg_uninit_image | `void sg_uninit_image(sg_image img)` | 4273 |
| sg_uninit_sampler | `void sg_uninit_sampler(sg_sampler smp)` | 4274 |
| sg_uninit_shader | `void sg_uninit_shader(sg_shader shd)` | 4275 |
| sg_uninit_pipeline | `void sg_uninit_pipeline(sg_pipeline pip)` | 4276 |
| sg_uninit_attachments | `void sg_uninit_attachments(sg_attachments atts)` | 4277 |
| sg_fail_buffer | `void sg_fail_buffer(sg_buffer buf)` | 4278 |
| sg_fail_image | `void sg_fail_image(sg_image img)` | 4279 |
| sg_fail_sampler | `void sg_fail_sampler(sg_sampler smp)` | 4280 |
| sg_fail_shader | `void sg_fail_shader(sg_shader shd)` | 4281 |
| sg_fail_pipeline | `void sg_fail_pipeline(sg_pipeline pip)` | 4282 |
| sg_fail_attachments | `void sg_fail_attachments(sg_attachments atts)` | 4283 |
| sg_enable_frame_stats | `void sg_enable_frame_stats(void)` | 4286 |
| sg_disable_frame_stats | `void sg_disable_frame_stats(void)` | 4287 |
| sg_frame_stats_enabled | `bool sg_frame_stats_enabled(void)` | 4288 |
| sg_query_frame_stats | `sg_frame_stats sg_query_frame_stats(void)` | 4289 |
| sg_d3d11_device | `const void* sg_d3d11_device(void)` | 4412 |
| sg_d3d11_device_context | `const void* sg_d3d11_device_context(void)` | 4414 |
| sg_d3d11_query_buffer_info | `sg_d3d11_buffer_info sg_d3d11_query_buffer_info(sg_buffer buf)` | 4416 |
| sg_d3d11_query_image_info | `sg_d3d11_image_info sg_d3d11_query_image_info(sg_image img)` | 4418 |
| sg_d3d11_query_sampler_info | `sg_d3d11_sampler_info sg_d3d11_query_sampler_info(sg_sampler smp)` | 4420 |
| sg_d3d11_query_shader_info | `sg_d3d11_shader_info sg_d3d11_query_shader_info(sg_shader shd)` | 4422 |
| sg_d3d11_query_pipeline_info | `sg_d3d11_pipeline_info sg_d3d11_query_pipeline_info(sg_pipeline pip)` | 4424 |
| sg_d3d11_query_attachments_info | `sg_d3d11_attachments_info sg_d3d11_query_attachments_info(sg_attachments atts)` | 4426 |
| sg_mtl_device | `const void* sg_mtl_device(void)` | 4429 |
| sg_mtl_render_command_encoder | `const void* sg_mtl_render_command_encoder(void)` | 4431 |
| sg_mtl_query_buffer_info | `sg_mtl_buffer_info sg_mtl_query_buffer_info(sg_buffer buf)` | 4433 |
| sg_mtl_query_image_info | `sg_mtl_image_info sg_mtl_query_image_info(sg_image img)` | 4435 |
| sg_mtl_query_sampler_info | `sg_mtl_sampler_info sg_mtl_query_sampler_info(sg_sampler smp)` | 4437 |
| sg_mtl_query_shader_info | `sg_mtl_shader_info sg_mtl_query_shader_info(sg_shader shd)` | 4439 |
| sg_mtl_query_pipeline_info | `sg_mtl_pipeline_info sg_mtl_query_pipeline_info(sg_pipeline pip)` | 4441 |
| sg_wgpu_device | `const void* sg_wgpu_device(void)` | 4444 |
| sg_wgpu_queue | `const void* sg_wgpu_queue(void)` | 4446 |
| sg_wgpu_command_encoder | `const void* sg_wgpu_command_encoder(void)` | 4448 |
| sg_wgpu_render_pass_encoder | `const void* sg_wgpu_render_pass_encoder(void)` | 4450 |
| sg_wgpu_query_buffer_info | `sg_wgpu_buffer_info sg_wgpu_query_buffer_info(sg_buffer buf)` | 4452 |
| sg_wgpu_query_image_info | `sg_wgpu_image_info sg_wgpu_query_image_info(sg_image img)` | 4454 |
| sg_wgpu_query_sampler_info | `sg_wgpu_sampler_info sg_wgpu_query_sampler_info(sg_sampler smp)` | 4456 |
| sg_wgpu_query_shader_info | `sg_wgpu_shader_info sg_wgpu_query_shader_info(sg_shader shd)` | 4458 |
| sg_wgpu_query_pipeline_info | `sg_wgpu_pipeline_info sg_wgpu_query_pipeline_info(sg_pipeline pip)` | 4460 |
| sg_wgpu_query_attachments_info | `sg_wgpu_attachments_info sg_wgpu_query_attachments_info(sg_attachments atts)` | 4462 |
| sg_gl_query_buffer_info | `sg_gl_buffer_info sg_gl_query_buffer_info(sg_buffer buf)` | 4465 |
| sg_gl_query_image_info | `sg_gl_image_info sg_gl_query_image_info(sg_image img)` | 4467 |
| sg_gl_query_sampler_info | `sg_gl_sampler_info sg_gl_query_sampler_info(sg_sampler smp)` | 4469 |
| sg_gl_query_shader_info | `sg_gl_shader_info sg_gl_query_shader_info(sg_shader shd)` | 4471 |
| sg_gl_query_attachments_info | `sg_gl_attachments_info sg_gl_query_attachments_info(sg_attachments atts)` | 4473 |

### sokol_app.h (Application Wrapper)
**File:** `C:\cosmo-sokol\deps\sokol\sokol_app.h`

| Function | Signature | Line |
|----------|-----------|------|
| sapp_isvalid | `bool sapp_isvalid(void)` | 1864 |
| sapp_width | `int sapp_width(void)` | 1866 |
| sapp_widthf | `float sapp_widthf(void)` | 1868 |
| sapp_height | `int sapp_height(void)` | 1870 |
| sapp_heightf | `float sapp_heightf(void)` | 1872 |
| sapp_color_format | `int sapp_color_format(void)` | 1874 |
| sapp_depth_format | `int sapp_depth_format(void)` | 1876 |
| sapp_sample_count | `int sapp_sample_count(void)` | 1878 |
| sapp_high_dpi | `bool sapp_high_dpi(void)` | 1880 |
| sapp_dpi_scale | `float sapp_dpi_scale(void)` | 1882 |
| sapp_show_keyboard | `void sapp_show_keyboard(bool show)` | 1884 |
| sapp_keyboard_shown | `bool sapp_keyboard_shown(void)` | 1886 |
| sapp_is_fullscreen | `bool sapp_is_fullscreen(void)` | 1888 |
| sapp_toggle_fullscreen | `void sapp_toggle_fullscreen(void)` | 1890 |
| sapp_show_mouse | `void sapp_show_mouse(bool show)` | 1892 |
| sapp_mouse_shown | `bool sapp_mouse_shown(void)` | 1894 |
| sapp_lock_mouse | `void sapp_lock_mouse(bool lock)` | 1896 |
| sapp_mouse_locked | `bool sapp_mouse_locked(void)` | 1898 |
| sapp_set_mouse_cursor | `void sapp_set_mouse_cursor(sapp_mouse_cursor cursor)` | 1900 |
| sapp_get_mouse_cursor | `sapp_mouse_cursor sapp_get_mouse_cursor(void)` | 1902 |
| sapp_userdata | `void* sapp_userdata(void)` | 1904 |
| sapp_query_desc | `sapp_desc sapp_query_desc(void)` | 1906 |
| sapp_request_quit | `void sapp_request_quit(void)` | 1908 |
| sapp_cancel_quit | `void sapp_cancel_quit(void)` | 1910 |
| sapp_quit | `void sapp_quit(void)` | 1912 |
| sapp_consume_event | `void sapp_consume_event(void)` | 1914 |
| sapp_frame_count | `uint64_t sapp_frame_count(void)` | 1916 |
| sapp_frame_duration | `double sapp_frame_duration(void)` | 1918 |
| sapp_set_clipboard_string | `void sapp_set_clipboard_string(const char* str)` | 1920 |
| sapp_get_clipboard_string | `const char* sapp_get_clipboard_string(void)` | 1922 |
| sapp_set_window_title | `void sapp_set_window_title(const char* str)` | 1924 |
| sapp_set_icon | `void sapp_set_icon(const sapp_icon_desc* icon_desc)` | 1926 |
| sapp_get_num_dropped_files | `int sapp_get_num_dropped_files(void)` | 1928 |
| sapp_get_dropped_file_path | `const char* sapp_get_dropped_file_path(int index)` | 1930 |
| sapp_run | `void sapp_run(const sapp_desc* desc)` | 1933 |
| sapp_egl_get_display | `const void* sapp_egl_get_display(void)` | 1936 |
| sapp_egl_get_context | `const void* sapp_egl_get_context(void)` | 1938 |
| sapp_html5_ask_leave_site | `void sapp_html5_ask_leave_site(bool ask)` | 1941 |
| sapp_html5_get_dropped_file_size | `uint32_t sapp_html5_get_dropped_file_size(int index)` | 1943 |
| sapp_html5_fetch_dropped_file | `void sapp_html5_fetch_dropped_file(const sapp_html5_fetch_request* request)` | 1945 |
| sapp_metal_get_device | `const void* sapp_metal_get_device(void)` | 1948 |
| sapp_metal_get_current_drawable | `const void* sapp_metal_get_current_drawable(void)` | 1950 |
| sapp_metal_get_depth_stencil_texture | `const void* sapp_metal_get_depth_stencil_texture(void)` | 1952 |
| sapp_metal_get_msaa_color_texture | `const void* sapp_metal_get_msaa_color_texture(void)` | 1954 |
| sapp_macos_get_window | `const void* sapp_macos_get_window(void)` | 1956 |
| sapp_ios_get_window | `const void* sapp_ios_get_window(void)` | 1958 |
| sapp_d3d11_get_device | `const void* sapp_d3d11_get_device(void)` | 1961 |
| sapp_d3d11_get_device_context | `const void* sapp_d3d11_get_device_context(void)` | 1963 |
| sapp_d3d11_get_swap_chain | `const void* sapp_d3d11_get_swap_chain(void)` | 1965 |
| sapp_d3d11_get_render_view | `const void* sapp_d3d11_get_render_view(void)` | 1967 |
| sapp_d3d11_get_resolve_view | `const void* sapp_d3d11_get_resolve_view(void)` | 1969 |
| sapp_d3d11_get_depth_stencil_view | `const void* sapp_d3d11_get_depth_stencil_view(void)` | 1971 |
| sapp_win32_get_hwnd | `const void* sapp_win32_get_hwnd(void)` | 1973 |
| sapp_wgpu_get_device | `const void* sapp_wgpu_get_device(void)` | 1976 |
| sapp_wgpu_get_render_view | `const void* sapp_wgpu_get_render_view(void)` | 1978 |
| sapp_wgpu_get_resolve_view | `const void* sapp_wgpu_get_resolve_view(void)` | 1980 |
| sapp_wgpu_get_depth_stencil_view | `const void* sapp_wgpu_get_depth_stencil_view(void)` | 1982 |
| sapp_gl_get_framebuffer | `uint32_t sapp_gl_get_framebuffer(void)` | 1985 |
| sapp_gl_get_major_version | `int sapp_gl_get_major_version(void)` | 1987 |
| sapp_gl_get_minor_version | `int sapp_gl_get_minor_version(void)` | 1989 |
| sapp_android_get_native_activity | `const void* sapp_android_get_native_activity(void)` | 1992 |

### sokol_audio.h (Audio)
**File:** `C:\cosmo-sokol\deps\sokol\sokol_audio.h`

| Function | Signature | Line |
|----------|-----------|------|
| saudio_setup | `void saudio_setup(const saudio_desc* desc)` | 604 |
| saudio_shutdown | `void saudio_shutdown(void)` | 606 |
| saudio_isvalid | `bool saudio_isvalid(void)` | 608 |
| saudio_userdata | `void* saudio_userdata(void)` | 610 |
| saudio_query_desc | `saudio_desc saudio_query_desc(void)` | 612 |
| saudio_sample_rate | `int saudio_sample_rate(void)` | 614 |
| saudio_buffer_frames | `int saudio_buffer_frames(void)` | 616 |
| saudio_channels | `int saudio_channels(void)` | 618 |
| saudio_suspended | `bool saudio_suspended(void)` | 620 |
| saudio_expect | `int saudio_expect(void)` | 622 |
| saudio_push | `int saudio_push(const float* frames, int num_frames)` | 624 |

### sokol_time.h (Timer)
**File:** `C:\cosmo-sokol\deps\sokol\sokol_time.h`

| Function | Signature | Line |
|----------|-----------|------|
| stm_setup | `void stm_setup(void)` | 128 |
| stm_now | `uint64_t stm_now(void)` | 129 |
| stm_diff | `uint64_t stm_diff(uint64_t new_ticks, uint64_t old_ticks)` | 130 |
| stm_since | `uint64_t stm_since(uint64_t start_ticks)` | 131 |
| stm_laptime | `uint64_t stm_laptime(uint64_t* last_time)` | 132 |
| stm_round_to_common_refresh_rate | `uint64_t stm_round_to_common_refresh_rate(uint64_t frame_ticks)` | 133 |
| stm_sec | `double stm_sec(uint64_t ticks)` | 134 |
| stm_ms | `double stm_ms(uint64_t ticks)` | 135 |
| stm_us | `double stm_us(uint64_t ticks)` | 136 |
| stm_ns | `double stm_ns(uint64_t ticks)` | 137 |

### sokol_fetch.h (Async File Loading)
**File:** `C:\cosmo-sokol\deps\sokol\sokol_fetch.h`

| Function | Signature | Line |
|----------|-----------|------|
| sfetch_setup | `void sfetch_setup(const sfetch_desc_t* desc)` | 1085 |
| sfetch_shutdown | `void sfetch_shutdown(void)` | 1087 |
| sfetch_valid | `bool sfetch_valid(void)` | 1089 |
| sfetch_desc | `sfetch_desc_t sfetch_desc(void)` | 1091 |
| sfetch_max_userdata_bytes | `int sfetch_max_userdata_bytes(void)` | 1093 |
| sfetch_max_path | `int sfetch_max_path(void)` | 1095 |
| sfetch_send | `sfetch_handle_t sfetch_send(const sfetch_request_t* request)` | 1098 |
| sfetch_handle_valid | `bool sfetch_handle_valid(sfetch_handle_t h)` | 1100 |
| sfetch_dowork | `void sfetch_dowork(void)` | 1102 |
| sfetch_bind_buffer | `void sfetch_bind_buffer(sfetch_handle_t h, sfetch_range_t buffer)` | 1105 |
| sfetch_unbind_buffer | `void* sfetch_unbind_buffer(sfetch_handle_t h)` | 1107 |
| sfetch_cancel | `void sfetch_cancel(sfetch_handle_t h)` | 1109 |
| sfetch_pause | `void sfetch_pause(sfetch_handle_t h)` | 1111 |
| sfetch_continue | `void sfetch_continue(sfetch_handle_t h)` | 1113 |

### sokol_args.h (Command Line Args)
**File:** `C:\cosmo-sokol\deps\sokol\sokol_args.h`

| Function | Signature | Line |
|----------|-----------|------|
| sargs_setup | `void sargs_setup(const sargs_desc* desc)` | 337 |
| sargs_shutdown | `void sargs_shutdown(void)` | 339 |
| sargs_isvalid | `bool sargs_isvalid(void)` | 341 |
| sargs_exists | `bool sargs_exists(const char* key)` | 343 |
| sargs_value | `const char* sargs_value(const char* key)` | 345 |
| sargs_value_def | `const char* sargs_value_def(const char* key, const char* def)` | 347 |
| sargs_equals | `bool sargs_equals(const char* key, const char* val)` | 349 |
| sargs_boolean | `bool sargs_boolean(const char* key)` | 351 |
| sargs_find | `int sargs_find(const char* key)` | 353 |
| sargs_num_args | `int sargs_num_args(void)` | 355 |
| sargs_key_at | `const char* sargs_key_at(int index)` | 357 |
| sargs_value_at | `const char* sargs_value_at(int index)` | 359 |

### sokol_log.h (Logging)
**File:** `C:\cosmo-sokol\deps\sokol\sokol_log.h`

| Function | Signature | Line |
|----------|-----------|------|
| slog_func | `void slog_func(const char* tag, uint32_t log_level, uint32_t log_item, const char* message, uint32_t line_nr, const char* filename, void* user_data)` | 134 |

### sokol_glue.h (App/Gfx Glue)
**File:** `C:\cosmo-sokol\deps\sokol\sokol_glue.h`

| Function | Signature | Line |
|----------|-----------|------|
| sglue_environment | `sg_environment sglue_environment(void)` | 106 |
| sglue_swapchain | `sg_swapchain sglue_swapchain(void)` | 107 |

### sokol_gl.h (OpenGL-style Immediate Mode)
**File:** `C:\cosmo-sokol\deps\sokol\util\sokol_gl.h`

| Function | Signature | Line |
|----------|-----------|------|
| sgl_setup | `void sgl_setup(const sgl_desc_t* desc)` | 831 |
| sgl_shutdown | `void sgl_shutdown(void)` | 832 |
| sgl_rad | `float sgl_rad(float deg)` | 833 |
| sgl_deg | `float sgl_deg(float rad)` | 834 |
| sgl_error | `sgl_error_t sgl_error(void)` | 835 |
| sgl_context_error | `sgl_error_t sgl_context_error(sgl_context ctx)` | 836 |
| sgl_make_context | `sgl_context sgl_make_context(const sgl_context_desc_t* desc)` | 839 |
| sgl_destroy_context | `void sgl_destroy_context(sgl_context ctx)` | 840 |
| sgl_set_context | `void sgl_set_context(sgl_context ctx)` | 841 |
| sgl_get_context | `sgl_context sgl_get_context(void)` | 842 |
| sgl_default_context | `sgl_context sgl_default_context(void)` | 843 |
| sgl_num_vertices | `int sgl_num_vertices(void)` | 846 |
| sgl_num_commands | `int sgl_num_commands(void)` | 847 |
| sgl_draw | `void sgl_draw(void)` | 850 |
| sgl_context_draw | `void sgl_context_draw(sgl_context ctx)` | 851 |
| sgl_draw_layer | `void sgl_draw_layer(int layer_id)` | 852 |
| sgl_context_draw_layer | `void sgl_context_draw_layer(sgl_context ctx, int layer_id)` | 853 |
| sgl_make_pipeline | `sgl_pipeline sgl_make_pipeline(const sg_pipeline_desc* desc)` | 856 |
| sgl_context_make_pipeline | `sgl_pipeline sgl_context_make_pipeline(sgl_context ctx, const sg_pipeline_desc* desc)` | 857 |
| sgl_destroy_pipeline | `void sgl_destroy_pipeline(sgl_pipeline pip)` | 858 |
| sgl_defaults | `void sgl_defaults(void)` | 861 |
| sgl_viewport | `void sgl_viewport(int x, int y, int w, int h, bool origin_top_left)` | 862 |
| sgl_viewportf | `void sgl_viewportf(float x, float y, float w, float h, bool origin_top_left)` | 863 |
| sgl_scissor_rect | `void sgl_scissor_rect(int x, int y, int w, int h, bool origin_top_left)` | 864 |
| sgl_scissor_rectf | `void sgl_scissor_rectf(float x, float y, float w, float h, bool origin_top_left)` | 865 |
| sgl_enable_texture | `void sgl_enable_texture(void)` | 866 |
| sgl_disable_texture | `void sgl_disable_texture(void)` | 867 |
| sgl_texture | `void sgl_texture(sg_image img, sg_sampler smp)` | 868 |
| sgl_layer | `void sgl_layer(int layer_id)` | 869 |
| sgl_load_default_pipeline | `void sgl_load_default_pipeline(void)` | 872 |
| sgl_load_pipeline | `void sgl_load_pipeline(sgl_pipeline pip)` | 873 |
| sgl_push_pipeline | `void sgl_push_pipeline(void)` | 874 |
| sgl_pop_pipeline | `void sgl_pop_pipeline(void)` | 875 |
| sgl_matrix_mode_modelview | `void sgl_matrix_mode_modelview(void)` | 878 |
| sgl_matrix_mode_projection | `void sgl_matrix_mode_projection(void)` | 879 |
| sgl_matrix_mode_texture | `void sgl_matrix_mode_texture(void)` | 880 |
| sgl_load_identity | `void sgl_load_identity(void)` | 881 |
| sgl_load_matrix | `void sgl_load_matrix(const float m[16])` | 882 |
| sgl_load_transpose_matrix | `void sgl_load_transpose_matrix(const float m[16])` | 883 |
| sgl_mult_matrix | `void sgl_mult_matrix(const float m[16])` | 884 |
| sgl_mult_transpose_matrix | `void sgl_mult_transpose_matrix(const float m[16])` | 885 |
| sgl_rotate | `void sgl_rotate(float angle_rad, float x, float y, float z)` | 886 |
| sgl_scale | `void sgl_scale(float x, float y, float z)` | 887 |
| sgl_translate | `void sgl_translate(float x, float y, float z)` | 888 |
| sgl_frustum | `void sgl_frustum(float l, float r, float b, float t, float n, float f)` | 889 |
| sgl_ortho | `void sgl_ortho(float l, float r, float b, float t, float n, float f)` | 890 |
| sgl_perspective | `void sgl_perspective(float fov_y, float aspect, float z_near, float z_far)` | 891 |
| sgl_lookat | `void sgl_lookat(float eye_x, float eye_y, float eye_z, float center_x, float center_y, float center_z, float up_x, float up_y, float up_z)` | 892 |
| sgl_push_matrix | `void sgl_push_matrix(void)` | 893 |
| sgl_pop_matrix | `void sgl_pop_matrix(void)` | 894 |
| sgl_t2f | `void sgl_t2f(float u, float v)` | 897 |
| sgl_c3f | `void sgl_c3f(float r, float g, float b)` | 898 |
| sgl_c4f | `void sgl_c4f(float r, float g, float b, float a)` | 899 |
| sgl_c3b | `void sgl_c3b(uint8_t r, uint8_t g, uint8_t b)` | 900 |
| sgl_c4b | `void sgl_c4b(uint8_t r, uint8_t g, uint8_t b, uint8_t a)` | 901 |
| sgl_c1i | `void sgl_c1i(uint32_t rgba)` | 902 |
| sgl_point_size | `void sgl_point_size(float s)` | 903 |
| sgl_begin_points | `void sgl_begin_points(void)` | 906 |
| sgl_begin_lines | `void sgl_begin_lines(void)` | 907 |
| sgl_begin_line_strip | `void sgl_begin_line_strip(void)` | 908 |
| sgl_begin_triangles | `void sgl_begin_triangles(void)` | 909 |
| sgl_begin_triangle_strip | `void sgl_begin_triangle_strip(void)` | 910 |
| sgl_begin_quads | `void sgl_begin_quads(void)` | 911 |
| sgl_v2f | `void sgl_v2f(float x, float y)` | 912 |
| sgl_v3f | `void sgl_v3f(float x, float y, float z)` | 913 |
| sgl_v2f_t2f | `void sgl_v2f_t2f(float x, float y, float u, float v)` | 914 |
| sgl_v3f_t2f | `void sgl_v3f_t2f(float x, float y, float z, float u, float v)` | 915 |
| sgl_v2f_c3f | `void sgl_v2f_c3f(float x, float y, float r, float g, float b)` | 916 |
| sgl_v2f_c3b | `void sgl_v2f_c3b(float x, float y, uint8_t r, uint8_t g, uint8_t b)` | 917 |
| sgl_v2f_c4f | `void sgl_v2f_c4f(float x, float y, float r, float g, float b, float a)` | 918 |
| sgl_v2f_c4b | `void sgl_v2f_c4b(float x, float y, uint8_t r, uint8_t g, uint8_t b, uint8_t a)` | 919 |
| sgl_v2f_c1i | `void sgl_v2f_c1i(float x, float y, uint32_t rgba)` | 920 |
| sgl_v3f_c3f | `void sgl_v3f_c3f(float x, float y, float z, float r, float g, float b)` | 921 |
| sgl_v3f_c3b | `void sgl_v3f_c3b(float x, float y, float z, uint8_t r, uint8_t g, uint8_t b)` | 922 |
| sgl_v3f_c4f | `void sgl_v3f_c4f(float x, float y, float z, float r, float g, float b, float a)` | 923 |
| sgl_v3f_c4b | `void sgl_v3f_c4b(float x, float y, float z, uint8_t r, uint8_t g, uint8_t b, uint8_t a)` | 924 |
| sgl_v3f_c1i | `void sgl_v3f_c1i(float x, float y, float z, uint32_t rgba)` | 925 |
| sgl_v2f_t2f_c3f | `void sgl_v2f_t2f_c3f(float x, float y, float u, float v, float r, float g, float b)` | 926 |
| sgl_v2f_t2f_c3b | `void sgl_v2f_t2f_c3b(float x, float y, float u, float v, uint8_t r, uint8_t g, uint8_t b)` | 927 |
| sgl_v2f_t2f_c4f | `void sgl_v2f_t2f_c4f(float x, float y, float u, float v, float r, float g, float b, float a)` | 928 |
| sgl_v2f_t2f_c4b | `void sgl_v2f_t2f_c4b(float x, float y, float u, float v, uint8_t r, uint8_t g, uint8_t b, uint8_t a)` | 929 |
| sgl_v2f_t2f_c1i | `void sgl_v2f_t2f_c1i(float x, float y, float u, float v, uint32_t rgba)` | 930 |
| sgl_v3f_t2f_c3f | `void sgl_v3f_t2f_c3f(float x, float y, float z, float u, float v, float r, float g, float b)` | 931 |
| sgl_v3f_t2f_c3b | `void sgl_v3f_t2f_c3b(float x, float y, float z, float u, float v, uint8_t r, uint8_t g, uint8_t b)` | 932 |
| sgl_v3f_t2f_c4f | `void sgl_v3f_t2f_c4f(float x, float y, float z, float u, float v, float r, float g, float b, float a)` | 933 |
| sgl_v3f_t2f_c4b | `void sgl_v3f_t2f_c4b(float x, float y, float z, float u, float v, uint8_t r, uint8_t g, uint8_t b, uint8_t a)` | 934 |
| sgl_v3f_t2f_c1i | `void sgl_v3f_t2f_c1i(float x, float y, float z, float u, float v, uint32_t rgba)` | 935 |
| sgl_end | `void sgl_end(void)` | 936 |

### sokol_debugtext.h (Debug Text Rendering)
**File:** `C:\cosmo-sokol\deps\sokol\util\sokol_debugtext.h`

| Function | Signature | Line |
|----------|-----------|------|
| sdtx_setup | `void sdtx_setup(const sdtx_desc_t* desc)` | 696 |
| sdtx_shutdown | `void sdtx_shutdown(void)` | 697 |
| sdtx_font_kc853 | `sdtx_font_desc_t sdtx_font_kc853(void)` | 700 |
| sdtx_font_kc854 | `sdtx_font_desc_t sdtx_font_kc854(void)` | 701 |
| sdtx_font_z1013 | `sdtx_font_desc_t sdtx_font_z1013(void)` | 702 |
| sdtx_font_cpc | `sdtx_font_desc_t sdtx_font_cpc(void)` | 703 |
| sdtx_font_c64 | `sdtx_font_desc_t sdtx_font_c64(void)` | 704 |
| sdtx_font_oric | `sdtx_font_desc_t sdtx_font_oric(void)` | 705 |
| sdtx_make_context | `sdtx_context sdtx_make_context(const sdtx_context_desc_t* desc)` | 708 |
| sdtx_destroy_context | `void sdtx_destroy_context(sdtx_context ctx)` | 709 |
| sdtx_set_context | `void sdtx_set_context(sdtx_context ctx)` | 710 |
| sdtx_get_context | `sdtx_context sdtx_get_context(void)` | 711 |
| sdtx_default_context | `sdtx_context sdtx_default_context(void)` | 712 |
| sdtx_draw | `void sdtx_draw(void)` | 715 |
| sdtx_context_draw | `void sdtx_context_draw(sdtx_context ctx)` | 716 |
| sdtx_draw_layer | `void sdtx_draw_layer(int layer_id)` | 717 |
| sdtx_context_draw_layer | `void sdtx_context_draw_layer(sdtx_context ctx, int layer_id)` | 718 |
| sdtx_layer | `void sdtx_layer(int layer_id)` | 721 |
| sdtx_font | `void sdtx_font(int font_index)` | 724 |
| sdtx_canvas | `void sdtx_canvas(float w, float h)` | 727 |
| sdtx_origin | `void sdtx_origin(float x, float y)` | 730 |
| sdtx_home | `void sdtx_home(void)` | 733 |
| sdtx_pos | `void sdtx_pos(float x, float y)` | 734 |
| sdtx_pos_x | `void sdtx_pos_x(float x)` | 735 |
| sdtx_pos_y | `void sdtx_pos_y(float y)` | 736 |
| sdtx_move | `void sdtx_move(float dx, float dy)` | 737 |
| sdtx_move_x | `void sdtx_move_x(float dx)` | 738 |
| sdtx_move_y | `void sdtx_move_y(float dy)` | 739 |
| sdtx_crlf | `void sdtx_crlf(void)` | 740 |
| sdtx_color3b | `void sdtx_color3b(uint8_t r, uint8_t g, uint8_t b)` | 743 |
| sdtx_color3f | `void sdtx_color3f(float r, float g, float b)` | 744 |
| sdtx_color4b | `void sdtx_color4b(uint8_t r, uint8_t g, uint8_t b, uint8_t a)` | 745 |
| sdtx_color4f | `void sdtx_color4f(float r, float g, float b, float a)` | 746 |
| sdtx_color1i | `void sdtx_color1i(uint32_t rgba)` | 747 |
| sdtx_putc | `void sdtx_putc(char c)` | 750 |
| sdtx_puts | `void sdtx_puts(const char* str)` | 751 |
| sdtx_putr | `void sdtx_putr(const char* str, int len)` | 752 |
| sdtx_printf | `int sdtx_printf(const char* fmt, ...)` | 753 |
| sdtx_vprintf | `int sdtx_vprintf(const char* fmt, va_list args)` | 754 |

### sokol_shape.h (3D Shape Generation)
**File:** `C:\cosmo-sokol\deps\sokol\util\sokol_shape.h`

| Function | Signature | Line |
|----------|-----------|------|
| sshape_build_plane | `sshape_buffer_t sshape_build_plane(const sshape_buffer_t* buf, const sshape_plane_t* params)` | 502 |
| sshape_build_box | `sshape_buffer_t sshape_build_box(const sshape_buffer_t* buf, const sshape_box_t* params)` | 503 |
| sshape_build_sphere | `sshape_buffer_t sshape_build_sphere(const sshape_buffer_t* buf, const sshape_sphere_t* params)` | 504 |
| sshape_build_cylinder | `sshape_buffer_t sshape_build_cylinder(const sshape_buffer_t* buf, const sshape_cylinder_t* params)` | 505 |
| sshape_build_torus | `sshape_buffer_t sshape_build_torus(const sshape_buffer_t* buf, const sshape_torus_t* params)` | 506 |
| sshape_plane_sizes | `sshape_sizes_t sshape_plane_sizes(uint32_t tiles)` | 509 |
| sshape_box_sizes | `sshape_sizes_t sshape_box_sizes(uint32_t tiles)` | 510 |
| sshape_sphere_sizes | `sshape_sizes_t sshape_sphere_sizes(uint32_t slices, uint32_t stacks)` | 511 |
| sshape_cylinder_sizes | `sshape_sizes_t sshape_cylinder_sizes(uint32_t slices, uint32_t stacks)` | 512 |
| sshape_torus_sizes | `sshape_sizes_t sshape_torus_sizes(uint32_t sides, uint32_t rings)` | 513 |
| sshape_element_range | `sshape_element_range_t sshape_element_range(const sshape_buffer_t* buf)` | 516 |
| sshape_vertex_buffer_desc | `sg_buffer_desc sshape_vertex_buffer_desc(const sshape_buffer_t* buf)` | 517 |
| sshape_index_buffer_desc | `sg_buffer_desc sshape_index_buffer_desc(const sshape_buffer_t* buf)` | 518 |
| sshape_vertex_buffer_layout_state | `sg_vertex_buffer_layout_state sshape_vertex_buffer_layout_state(void)` | 519 |
| sshape_position_vertex_attr_state | `sg_vertex_attr_state sshape_position_vertex_attr_state(void)` | 520 |
| sshape_normal_vertex_attr_state | `sg_vertex_attr_state sshape_normal_vertex_attr_state(void)` | 521 |
| sshape_texcoord_vertex_attr_state | `sg_vertex_attr_state sshape_texcoord_vertex_attr_state(void)` | 522 |
| sshape_color_vertex_attr_state | `sg_vertex_attr_state sshape_color_vertex_attr_state(void)` | 523 |
| sshape_color_4f | `uint32_t sshape_color_4f(float r, float g, float b, float a)` | 526 |
| sshape_color_3f | `uint32_t sshape_color_3f(float r, float g, float b)` | 527 |
| sshape_color_4b | `uint32_t sshape_color_4b(uint8_t r, uint8_t g, uint8_t b, uint8_t a)` | 528 |
| sshape_color_3b | `uint32_t sshape_color_3b(uint8_t r, uint8_t g, uint8_t b)` | 529 |
| sshape_mat4 | `sshape_mat4_t sshape_mat4(const float m[16])` | 532 |
| sshape_mat4_transpose | `sshape_mat4_t sshape_mat4_transpose(const float m[16])` | 533 |

### sokol_color.h (Color Utilities)
**File:** `C:\cosmo-sokol\deps\sokol\util\sokol_color.h`

| Function | Signature | Line |
|----------|-----------|------|
| sg_make_color_4b | `sg_color sg_make_color_4b(uint8_t r, uint8_t g, uint8_t b, uint8_t a)` | 155 |
| sg_make_color_1i | `sg_color sg_make_color_1i(uint32_t rgba)` | 156 |
| sg_color_lerp | `sg_color sg_color_lerp(const sg_color* color_a, const sg_color* color_b, float amount)` | 157 |
| sg_color_lerp_precise | `sg_color sg_color_lerp_precise(const sg_color* color_a, const sg_color* color_b, float amount)` | 158 |
| sg_color_multiply | `sg_color sg_color_multiply(const sg_color* color, float scale)` | 159 |

---

## FUNCTION MANIFEST: Fork-Specific Code

### main.c (Demo Application)
**File:** `C:\cosmo-sokol\main.c`

| Function | Signature | Line |
|----------|-----------|------|
| init | `void init(void)` | 27 |
| frame | `void frame(void)` | 45 |
| cleanup | `void cleanup(void)` | 89 |
| input | `void input(const sapp_event* event)` | 94 |
| main | `int main(int argc, char* argv[])` | 98 |

### win32_tweaks.c (Windows Console Hiding)
**File:** `C:\cosmo-sokol\win32_tweaks.c`

| Function | Signature | Line |
|----------|-----------|------|
| win32_tweaks_hide_console | `void win32_tweaks_hide_console(void)` | 4 |

### win32_tweaks.h (Windows Console Hiding Header)
**File:** `C:\cosmo-sokol\win32_tweaks.h`

| Function | Signature | Line |
|----------|-----------|------|
| win32_tweaks_hide_console | `void win32_tweaks_hide_console(void)` | 5 |

### nvapi.c (NVIDIA Driver Optimization)
**File:** `C:\cosmo-sokol\nvapi\nvapi.c`

| Function | Signature | Line |
|----------|-----------|------|
| nvapi_disable_threaded_optimization | `bool nvapi_disable_threaded_optimization(const char* profile_name)` | 44 |

### nvapi.h (NVIDIA Header)
**File:** `C:\cosmo-sokol\nvapi\nvapi.h`

| Function | Signature | Line |
|----------|-----------|------|
| nvapi_disable_threaded_optimization | `bool nvapi_disable_threaded_optimization(const char* profile_name)` | 7 |

### sokol_cosmo.c (Runtime Dispatch Layer)
**File:** `C:\cosmo-sokol\shims\sokol\sokol_cosmo.c`

This file contains **dispatch wrappers** for ALL sokol_app and sokol_gfx functions. Each function dispatches to `linux_*`, `windows_*`, or `macos_*` prefixed versions based on `IsLinux()`, `IsWindows()`, `IsXnu()`.

**Pattern for each function (example at line 10):**
```c
bool sapp_isvalid(void) {
    if (IsLinux()) { return linux_sapp_isvalid(); }
    if (IsWindows()) { return windows_sapp_isvalid(); }
    if (IsXnu()) { return macos_sapp_isvalid(); }
}
```

**Dispatched Functions (lines 10-3099):**
- All 64 sapp_* functions
- All 110+ sg_* functions

### sokol_macos.c (macOS Stubs)
**File:** `C:\cosmo-sokol\shims\sokol\sokol_macos.c`

Contains **stub implementations** for all macos_sapp_* and macos_sg_* functions. Currently not implemented (requires Objective-C runtime).

| Function | Signature | Line |
|----------|-----------|------|
| _macos_not_implemented | `static void _macos_not_implemented(const char* func)` | 52 |
| macos_sapp_isvalid | `bool macos_sapp_isvalid(void)` | 69 |
| macos_sapp_width | `int macos_sapp_width(void)` | 73 |
| macos_sapp_widthf | `float macos_sapp_widthf(void)` | 77 |
| macos_sapp_height | `int macos_sapp_height(void)` | 81 |
| macos_sapp_heightf | `float macos_sapp_heightf(void)` | 85 |
| macos_sapp_run | `void macos_sapp_run(const sapp_desc* desc)` | 185 |
| macos_sg_setup | `void macos_sg_setup(const sg_desc* desc)` | 269 |
| *(+170 more stub functions)* | | |

### shims/linux/x11.c (X11 Dynamic Loading)
**File:** `C:\cosmo-sokol\shims\linux\x11.c`

Shim functions that load X11 functions via `cosmo_dlopen("libX11.so")`:

| Function | Signature | Line |
|----------|-----------|------|
| load_X11_procs | `static void load_X11_procs(void)` | 85 |
| load_Xcursor_procs | `static void load_Xcursor_procs(void)` | 151 |
| load_Xi_procs | `static void load_Xi_procs(void)` | 165 |
| XOpenDisplay | `Display* XOpenDisplay(const char* display_name)` | 172 |
| XCloseDisplay | `int XCloseDisplay(Display* display)` | 178 |
| XFlush | `int XFlush(Display* display)` | 184 |
| XNextEvent | `int XNextEvent(Display* display, XEvent* event_return)` | 190 |
| XPending | `int XPending(Display* display)` | 196 |
| *(+50 more X11 wrapper functions)* | | |

### shims/linux/gl.c (OpenGL Dynamic Loading)
**File:** `C:\cosmo-sokol\shims\linux\gl.c`

Shim functions that load OpenGL via `dlopen("libGL.so")`:

Contains 600+ OpenGL function pointers and wrapper functions (lines 1-6172).

---

## Upstream Tracking Information

### floooh/sokol (Primary Upstream)
- **Repository:** https://github.com/floooh/sokol
- **License:** zlib/libpng
- **Local Path:** `C:\cosmo-sokol\deps\sokol\`
- **Key Files:**
  - `sokol_app.h` - 12,311 lines
  - `sokol_gfx.h` - 19,858 lines
  - `sokol_audio.h` - Audio backend
  - `sokol_time.h`, `sokol_fetch.h`, `sokol_args.h`, `sokol_log.h`, `sokol_glue.h`
  - `util/sokol_gl.h`, `util/sokol_debugtext.h`, `util/sokol_shape.h`, `util/sokol_color.h`

### jart/cosmopolitan (Build Toolchain)
- **Repository:** https://github.com/jart/cosmopolitan
- **Purpose:** Provides `cosmocc` compiler, `cosmo_dlopen()`, `IsLinux()/IsWindows()/IsXnu()` detection
- **Key Dependencies:**
  - `<cosmo.h>` - Platform detection macros
  - `<windowsesque.h>` - Win32 type compatibility
  - `cosmo_dlopen()`, `cosmo_dlsym()`, `cosmo_dltramp()` - Dynamic loading

---

## Architecture Notes

### Platform Dispatch Pattern

1. **Symbol Renaming Headers** (`sokol_linux.h`, `sokol_windows.h`, `sokol_macos.h`):
   - Define macros like `#define sapp_isvalid linux_sapp_isvalid`
   - Included before sokol headers to create platform-specific symbols

2. **Dispatch Layer** (`sokol_cosmo.c`):
   - Provides canonical `sapp_*` and `sg_*` symbols
   - Uses runtime platform detection to call correct prefix

3. **Platform Builds**:
   - `sokol_linux.c` - Compiles sokol with Linux/X11/GLX
   - `sokol_windows.c` - Compiles sokol with Win32/WGL
   - `sokol_macos.c` - Stub (needs Objective-C runtime implementation)

### Dynamic Library Shims (Linux)
- X11 functions loaded from `libX11.so`, `libXcursor.so`, `libXi.so`
- OpenGL functions loaded from `libGL.so`
- Uses `cosmo_dltramp()` for function trampolines

---

## Summary Statistics

| Category | Count |
|----------|-------|
| **Upstream Sokol Functions** | 300+ |
| **Fork-Specific Functions** | 15 |
| **Platform Dispatch Wrappers** | 174 |
| **macOS Stub Functions** | 174 |
| **X11 Shim Functions** | 55 |
| **OpenGL Shim Functions** | 600+ |
| **Total Source Files** | 110+ |

---

*Report generated by seeker specialist for Swiss Rounds analysis.*
