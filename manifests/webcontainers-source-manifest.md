# WebContainers Source Manifest

Generated: 2026-02-11
Source: https://github.com/stackblitz/webcontainer-core @ main
Path: `C:\webcontainer-core`

## ⚠️ IMPORTANT: Closed Source

**WebContainers is proprietary.** The `webcontainer-core` repo is an issues-only repository. The actual implementation is closed-source, owned by StackBlitz.

## Overview

WebContainers run Node.js natively in the browser using WebAssembly. Boots in milliseconds. Used by Bolt.new for instant dev environments.

## Public API (from npm package)

Package: `@webcontainer/api`

### Core Types
| Type | Purpose |
|------|---------|
| `WebContainer` | Main container instance |
| `WebContainerProcess` | Running process handle |
| `FileSystemTree` | Directory/file structure |
| `SpawnOptions` | Process spawn options |
| `Terminal` | Terminal emulator interface |

### WebContainer Class
| Method | Signature | Purpose |
|--------|-----------|---------|
| `WebContainer.boot()` | `static async () -> WebContainer` | Boot container instance |
| `container.mount()` | `async (FileSystemTree) -> void` | Mount filesystem |
| `container.spawn()` | `async (cmd, args, opts) -> WebContainerProcess` | Spawn process |
| `container.fs` | `FileSystemAPI` | Filesystem access |
| `container.on('server-ready', cb)` | Event | Server started |
| `container.on('error', cb)` | Event | Container error |
| `container.teardown()` | `() -> void` | Destroy container |

### FileSystemAPI
| Method | Signature | Purpose |
|--------|-----------|---------|
| `fs.readFile()` | `async (path, encoding?) -> string|Uint8Array` | Read file |
| `fs.writeFile()` | `async (path, data, opts?) -> void` | Write file |
| `fs.readdir()` | `async (path, opts?) -> string[]` | List directory |
| `fs.mkdir()` | `async (path, opts?) -> void` | Create directory |
| `fs.rm()` | `async (path, opts?) -> void` | Remove file/dir |

### WebContainerProcess
| Property/Method | Purpose |
|-----------------|---------|
| `process.exit` | Promise that resolves with exit code |
| `process.output` | ReadableStream of stdout/stderr |
| `process.input` | WritableStream for stdin |
| `process.kill()` | Kill the process |

## Usage Pattern (from Bolt.new)

```typescript
import { WebContainer } from '@webcontainer/api';

// Boot container
const container = await WebContainer.boot();

// Mount project files
await container.mount({
  'package.json': {
    file: { contents: '{"name": "app"}' }
  },
  'index.js': {
    file: { contents: 'console.log("hello")' }
  },
  'node_modules': { directory: {} }
});

// Install dependencies
const installProcess = await container.spawn('npm', ['install']);
await installProcess.exit;

// Run dev server
const devProcess = await container.spawn('npm', ['run', 'dev']);

// Listen for server ready
container.on('server-ready', (port, url) => {
  console.log(`Server at ${url}`);
});
```

## Browser Requirements

- SharedArrayBuffer (requires cross-origin isolation)
- Service Workers
- WebAssembly
- Chrome 89+, Firefox 89+, Safari 16.4+

### Required Headers
```
Cross-Origin-Embedder-Policy: require-corp
Cross-Origin-Opener-Policy: same-origin
```

## What DOES Exist (Known from Bolt.new)

- ✅ Full Node.js runtime in browser
- ✅ npm/pnpm/yarn package management
- ✅ File system API
- ✅ Process spawning
- ✅ Terminal I/O
- ✅ Dev server with port forwarding
- ✅ Fast boot (<1 second)

## What Does NOT Exist

- ❌ **No source code** — proprietary
- ❌ No Python/Ruby/other runtimes
- ❌ No Docker containers
- ❌ No GPU access
- ❌ No native modules (pure JS only)
- ❌ No network access outside container (except dev server)
- ❌ No persistent storage (in-memory only)

## Alternatives (Open Source)

| Project | Description |
|---------|-------------|
| **wasm-git** | Git in browser via WASM |
| **browser-fs-access** | File system access API |
| **xterm.js** | Terminal emulator |
| **wasi-sdk** | WASI toolchain |
| **wasmtime** | WASM runtime (not browser) |

## Documentation

- Main docs: https://webcontainers.io
- API reference: https://webcontainers.io/api
- Enterprise: https://webcontainers.io/enterprise

---

*This manifest notes that WebContainers is closed-source. Only public API documented.*
