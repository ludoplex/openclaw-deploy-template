# Sokol Web/WASM Support & Examples Review

**Date:** 2026-02-06  
**Source:** https://github.com/floooh/sokol-samples

## 1. Emscripten/WASM Build Support

### Overview
Sokol has **first-class WebGL2/WebGPU support** via Emscripten. The build system uses `fips` (a cmake-based meta build system) with pre-configured WASM targets.

### Available WASM Build Configurations

| Config | Backend | Description |
|--------|---------|-------------|
| `sapp-webgl2-wasm-ninja-debug` | WebGL2 | Debug build with WASM |
| `sapp-webgl2-wasm-ninja-release` | WebGL2 | Optimized release |
| `sapp-wgpu-wasm-ninja-debug` | WebGPU | Debug with WebGPU |
| `sapp-wgpu-wasm-ninja-release` | WebGPU | WebGPU optimized |
| `webgl2-wasm-ninja-*` | WebGL2 | Platform-specific samples |

### WASM Build Configuration (fips)
```yaml
# From sapp-webgl2-wasm-ninja-release.yml
platform: emscripten
generator: Ninja
build_tool: ninja
build_type: Release
cmake-toolchain: emscripten.toolchain.cmake
defines:
    USE_SOKOL_APP: ON
    FIPS_EMSCRIPTEN_USE_WASM: ON
    FIPS_EMSCRIPTEN_USE_WEBGL2: ON
    FIPS_EMSCRIPTEN_USE_EMMALLOC: ON
    FIPS_EMSCRIPTEN_RELATIVE_SHELL_HTML: "webpage/shell.html"
    FIPS_EMSCRIPTEN_USE_CLOSURE: ON
```

### Manual Emscripten Build (No Build System)
```bash
# For html5/ samples (platform-specific):
emcc cube-emsc.c -o cube-emsc.html -I../../sokol -sUSE_WEBGL2 --shell-file=../webpage/shell.html

# For sapp/ samples (cross-platform):
sokol-shdc -i cube-sapp.glsl -o cube-sapp.glsl.h -l glsl300es
emcc cube-sapp.c ../libs/sokol/sokol.c -o cube-sapp.html \
    -DSOKOL_GLES3 -I../../sokol -I../libs \
    -sUSE_WEBGL2 --shell-file=../webpage/shell.html
```

### Key Emscripten Integration Points

#### `emsc.h` Helper (for html5/ samples)
```c
// Initialize WebGL2 context on canvas
emsc_init("#canvas", EMSC_ANTIALIAS);

// Get swapchain for sokol_gfx
sg_swapchain emsc_swapchain(void);
sg_environment emsc_environment(void);
```

#### sokol_app.h (for sapp/ samples)
sokol_app.h handles all Emscripten integration automatically:
- Canvas setup
- Input events (mouse, keyboard, touch)
- Resize handling
- Main loop via `emscripten_request_animation_frame_loop`

### Backend Define for WebGL2
```c
#define SOKOL_GLES3  // WebGL2 uses GLES3 API
```

### Live Demos
- **WebGL2:** https://floooh.github.io/sokol-html5/index.html
- **WebGPU:** https://floooh.github.io/sokol-webgpu/index.html

---

## 2. Sokol + Dear ImGui Integration

### Three Approaches Available

#### A) Using `sokol_imgui.h` (Recommended)
The official integration header handles everything:
- Vertex/index buffer management
- Font texture atlas
- Input event routing
- Multi-platform shader code

**C++ Example (`sapp/imgui-sapp.cc`):**
```cpp
#include "sokol_app.h"
#include "sokol_gfx.h"
#include "sokol_glue.h"
#include "imgui.h"
#define SOKOL_IMGUI_IMPL
#include "sokol_imgui.h"

void init(void) {
    sg_setup(&(sg_desc){ .environment = sglue_environment() });
    simgui_setup(&(simgui_desc_t){ .logger.func = slog_func });
}

void frame(void) {
    simgui_new_frame({ sapp_width(), sapp_height(), sapp_frame_duration(), sapp_dpi_scale() });
    
    // Dear ImGui calls here
    ImGui::Text("Hello!");
    
    sg_begin_pass(&(sg_pass){ .action = pass_action, .swapchain = sglue_swapchain() });
    simgui_render();
    sg_end_pass();
    sg_commit();
}

void input(const sapp_event* event) {
    simgui_handle_event(event);
}
```

#### B) Using `cimgui.h` (C bindings)
**C Example (`sapp/cimgui-sapp.c`):**
```c
#include "cimgui.h"
#define SOKOL_IMGUI_IMPL
#include "sokol_imgui.h"

void frame(void) {
    simgui_new_frame(&(simgui_frame_desc_t){
        .width = sapp_width(),
        .height = sapp_height(),
        .delta_time = sapp_frame_duration(),
        .dpi_scale = sapp_dpi_scale()
    });
    
    igText("Hello from C!");
    igSliderFloatEx("float", &f, 0.0f, 1.0f, "%.3f", ImGuiSliderFlags_None);
    // ...
}
```

#### C) Manual Integration (html5/ samples)
The `html5/imgui-emsc.cc` shows manual ImGui integration with Emscripten callbacks for input:
```cpp
// Manual input forwarding
emscripten_set_keydown_callback(EMSCRIPTEN_EVENT_TARGET_WINDOW, nullptr, true,
    [](int, const EmscriptenKeyboardEvent* e, void*)->EM_BOOL {
        ImGui::GetIO().AddKeyEvent(as_imgui_key(e->keyCode), true);
        return e->keyCode < 32;
    });
// ... mouse, wheel callbacks
```

### Debug UI Overlay Pattern (`dbgui/`)
A reusable debug overlay combining:
- `sokol_imgui.h` - ImGui rendering
- `sokol_gfx_imgui.h` - sokol_gfx inspection UI

```cpp
// dbgui.cc
void __dbgui_setup(int sample_count) {
    sgimgui_setup(&desc);
    simgui_setup(&simgui_desc);
}

void __dbgui_draw(void) {
    simgui_new_frame({ sapp_width(), sapp_height(), sapp_frame_duration(), sapp_dpi_scale() });
    if (ImGui::BeginMainMenuBar()) {
        sgimgui_draw_menu("sokol-gfx");
        ImGui::EndMainMenuBar();
    }
    sgimgui_draw();
    simgui_render();
}
```

---

## 3. Example Patterns from sokol-samples

### Directory Structure

```
sokol-samples/
├── html5/           # Platform-specific Emscripten samples (use emsc.h)
├── sapp/            # Cross-platform samples using sokol_app.h
├── glfw/            # Desktop GLFW samples
├── d3d11/           # Windows D3D11 samples
├── metal/           # macOS/iOS Metal samples
├── libs/
│   ├── sokol/       # Compiled sokol implementation
│   ├── dbgui/       # Debug UI overlay
│   └── ...          # Third-party libs
└── webpage/
    ├── shell.html   # Minimal HTML shell template
    └── wasm.html    # Full page template with nav
```

### Key ImGui Samples

| Sample | Description | Link |
|--------|-------------|------|
| `imgui-sapp.cc` | Basic Dear ImGui demo (C++) | [Demo](https://floooh.github.io/sokol-html5/imgui-sapp.html) |
| `cimgui-sapp.c` | C bindings version | [Demo](https://floooh.github.io/sokol-html5/cimgui-sapp.html) |
| `imgui-dock-sapp.cc` | ImGui docking support | [Demo](https://floooh.github.io/sokol-html5/imgui-dock-sapp.html) |
| `imgui-highdpi-sapp.cc` | High DPI handling | [Demo](https://floooh.github.io/sokol-html5/imgui-highdpi-sapp.html) |
| `imgui-images-sapp.c` | Custom textures in ImGui | [Demo](https://floooh.github.io/sokol-html5/imgui-images-sapp.html) |
| `imgui-usercallback-sapp.c` | Custom draw callbacks | [Demo](https://floooh.github.io/sokol-html5/imgui-usercallback-sapp.html) |

### HTML Shell Template (Minimal)
```html
<!doctype html>
<html lang="en-us">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"/>
    <style>
        body { margin: 0; background-color: black }
        .game {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            overflow: hidden;
        }
    </style>
</head>
<body>
    <canvas class="game" id="canvas" oncontextmenu="event.preventDefault()"></canvas>
    <script type='text/javascript'>
        var Module = {
            print: (...args) => console.log('[stdout]: ' + args.join(' ')),
            printErr: (...args) => console.log('[stderr]: ' + args.join(' ')),
        };
    </script>
    {{{ SCRIPT }}}
</body>
</html>
```

### Sokol Implementation Pattern
All sokol headers are compiled in a single translation unit:
```c
// sokol.c
#define SOKOL_IMPL
#define SOKOL_TRACE_HOOKS  // For debug inspection
#include "sokol_app.h"
#include "sokol_gfx.h"
#include "sokol_time.h"
#include "sokol_audio.h"
#include "sokol_fetch.h"
#include "sokol_log.h"
#include "sokol_glue.h"
```

### Other Useful UI Samples

| Sample | UI Library | Description |
|--------|------------|-------------|
| `sgl-microui-sapp.c` | [microui](https://github.com/rxi/microui) | Lightweight immediate-mode UI |
| `nuklear-sapp.c` | [Nuklear](https://github.com/vurtun/nuklear) | Another IMGUI alternative |
| `debugtext-sapp.c` | sokol_debugtext.h | Simple text rendering |
| `fontstash-sapp.c` | fontstash | TrueType font rendering |

---

## 4. Key Takeaways for Our Project

### Recommended Approach
1. Use `sokol_app.h` for cross-platform window/input handling
2. Use `sokol_gfx.h` with `SOKOL_GLES3` for WebGL2
3. Use `sokol_imgui.h` for Dear ImGui integration
4. Use `sokol-shdc` for cross-compiling shaders to GLSL ES 3.0

### Minimal WASM Build Command
```bash
emcc app.c sokol.c -o app.html \
    -DSOKOL_GLES3 \
    -I./sokol \
    -sUSE_WEBGL2 \
    -sALLOW_MEMORY_GROWTH \
    --shell-file=shell.html
```

### Dependencies to Clone
```bash
git clone https://github.com/floooh/sokol          # Core headers
git clone https://github.com/floooh/sokol-tools-bin # Shader compiler
git clone https://github.com/floooh/dcimgui        # Dear ImGui C bindings (optional)
```

### fips Build System
If using fips for full build automation:
```bash
./fips setup emscripten  # Install Emscripten SDK
./fips set config sapp-webgl2-wasm-ninja-release
./fips build
./fips run imgui-sapp
```
