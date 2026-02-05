# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

Built with [Cosmopolitan Libc](https://github.com/jart/cosmopolitan) — single portable binary.

## Quick Start

```bash
make native
./build/{{ cookiecutter.project_slug }}

# Run tests
make test

# Build APE (runs on Linux/Mac/Windows/BSD)
make cosmo
./dist/{{ cookiecutter.project_slug }}.com
```

## Build Targets

| Target | Description |
|--------|-------------|
| `make native` | Build with system compiler |
| `make cosmo` | Build portable APE binary |
| `make test` | Run tests |
| `make test-san` | Run with ASAN + UBSAN |
| `make cppcheck` | Static analysis |
| `make lint` | All linters |
| `make clean` | Remove build artifacts |

{% if cookiecutter.use_sqlite == "yes" %}
## SQLite

Bundled SQLite for APE builds (auto-downloaded). Native builds use system `-lsqlite3`.
{% endif %}

## License

{{ cookiecutter.license }}{% if cookiecutter.author %} — {{ cookiecutter.author }}{% endif %}
