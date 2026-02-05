# {{ cookiecutter.project_name }} — Makefile
# Cosmopolitan C project{% if cookiecutter.use_sqlite == "yes" %} with SQLite{% endif %}

CC_NATIVE ?= cc
CFLAGS    := -O2 -Wall -Wextra -Werror -std=c11 -DNATIVE_BUILD
LDFLAGS   :={% if cookiecutter.use_sqlite == "yes" %} -lsqlite3{% endif %}

SRC_DIR   := src
BUILD_DIR := build
DIST_DIR  := dist

SRCS      := $(SRC_DIR)/main.c{% if cookiecutter.use_sqlite == "yes" %} $(SRC_DIR)/db/database.c{% endif %}

COSMOCC   ?= cosmocc
{% if cookiecutter.use_sqlite == "yes" %}
SQLITE_VER    := 3480000
SQLITE_URL    := https://www.sqlite.org/2025/sqlite-amalgamation-$(SQLITE_VER).zip
SQLITE_SRC    := vendor/sqlite/sqlite3.c
SQLITE_FLAGS  := -DSQLITE_THREADSAFE=0 -DSQLITE_OMIT_LOAD_EXTENSION
{% endif %}
.PHONY: all native cosmo test test-asan test-ubsan test-san asan ubsan san \
        cppcheck clang-tidy lint install uninstall clean schema help

all: native

help:
	@echo "{{ cookiecutter.project_name }}"
	@echo ""
	@echo "  make native      Build with system compiler (default)"
	@echo "  make cosmo       Build APE binary with cosmocc"
	@echo "  make test        Run tests"
	@echo "  make test-san    Run tests with ASAN+UBSAN"
	@echo "  make cppcheck    Run static analysis"
	@echo "  make lint        Run all linters"
	@echo "  make clean       Remove build artifacts"

# ── Native build ──────────────────────────────────────────
native: | $(BUILD_DIR)
{% if cookiecutter.use_sqlite == "yes" %}
	@if [ -f $(SQLITE_SRC) ]; then \
		echo "Building with bundled SQLite..."; \
		$(CC_NATIVE) $(CFLAGS) $(SQLITE_FLAGS) -Ivendor/sqlite \
			-o $(BUILD_DIR)/{{ cookiecutter.project_slug }} $(SRCS) $(SQLITE_SRC) -lm; \
	else \
		echo "Building with system SQLite (-lsqlite3)..."; \
		$(CC_NATIVE) $(CFLAGS) -o $(BUILD_DIR)/{{ cookiecutter.project_slug }} $(SRCS) $(LDFLAGS) -lm; \
	fi
{% else %}
	$(CC_NATIVE) $(CFLAGS) -o $(BUILD_DIR)/{{ cookiecutter.project_slug }} $(SRCS) $(LDFLAGS) -lm
{% endif %}
	@echo "Built: $(BUILD_DIR)/{{ cookiecutter.project_slug }}"

# ── Cosmopolitan APE build ────────────────────────────────
{% if cookiecutter.use_sqlite == "yes" %}
cosmo: $(SQLITE_SRC) | $(DIST_DIR)
	$(COSMOCC) $(CFLAGS) $(SQLITE_FLAGS) -Ivendor/sqlite \
		-o $(DIST_DIR)/{{ cookiecutter.project_slug }}.com $(SRCS) $(SQLITE_SRC) -lm
{% else %}
cosmo: | $(DIST_DIR)
	$(COSMOCC) $(CFLAGS) -o $(DIST_DIR)/{{ cookiecutter.project_slug }}.com $(SRCS) -lm
{% endif %}
	@echo "Built APE: $(DIST_DIR)/{{ cookiecutter.project_slug }}.com"

# ── Tests ─────────────────────────────────────────────────
test: native | $(BUILD_DIR)
	$(CC_NATIVE) $(CFLAGS) -Isrc -o $(BUILD_DIR)/test_main tests/test_main.c{% if cookiecutter.use_sqlite == "yes" %} $(SRC_DIR)/db/database.c $(LDFLAGS){% endif %} -lm
	$(BUILD_DIR)/test_main

test-asan: | $(BUILD_DIR)
	$(CC_NATIVE) $(CFLAGS) -fsanitize=address -fno-omit-frame-pointer -Isrc \
		-o $(BUILD_DIR)/test_main_asan tests/test_main.c{% if cookiecutter.use_sqlite == "yes" %} $(SRC_DIR)/db/database.c $(LDFLAGS){% endif %} -lm
	$(BUILD_DIR)/test_main_asan

test-ubsan: | $(BUILD_DIR)
	$(CC_NATIVE) $(CFLAGS) -fsanitize=undefined -fno-omit-frame-pointer -Isrc \
		-o $(BUILD_DIR)/test_main_ubsan tests/test_main.c{% if cookiecutter.use_sqlite == "yes" %} $(SRC_DIR)/db/database.c $(LDFLAGS){% endif %} -lm
	$(BUILD_DIR)/test_main_ubsan

test-san: test-asan test-ubsan

asan: test-asan
ubsan: test-ubsan
san: test-san

# ── Static analysis ───────────────────────────────────────
cppcheck:
	cppcheck --enable=warning,style,performance,portability \
		--error-exitcode=1 --suppress=missingIncludeSystem \
		-I src src/

clang-tidy:
	clang-tidy src/*.c{% if cookiecutter.use_sqlite == "yes" %} src/db/*.c{% endif %} -- $(CFLAGS) -Isrc

lint: cppcheck

# ── Install ───────────────────────────────────────────────
PREFIX  ?= /usr/local
DESTDIR ?=

install: native
	install -d $(DESTDIR)$(PREFIX)/bin
	install -m 755 $(BUILD_DIR)/{{ cookiecutter.project_slug }} $(DESTDIR)$(PREFIX)/bin/

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/{{ cookiecutter.project_slug }}
{% if cookiecutter.use_sqlite == "yes" %}
# ── Schema ────────────────────────────────────────────────
schema:
	@echo "Generating embedded schema header..."
	@printf 'static const char *EMBEDDED_SCHEMA =\n' > src/db/schema_sql.h
	@sed 's/"/\\"/g; s/^/    "/; s/$$/\\n"/' src/db/schema.sql >> src/db/schema_sql.h
	@printf ';\n' >> src/db/schema_sql.h

# ── Vendor fetch ──────────────────────────────────────────
$(SQLITE_SRC):
	mkdir -p vendor/sqlite
	curl -L -o /tmp/sqlite.zip $(SQLITE_URL)
	unzip -o /tmp/sqlite.zip -d /tmp/sqlite-tmp
	cp /tmp/sqlite-tmp/sqlite-amalgamation-$(SQLITE_VER)/sqlite3.c vendor/sqlite/
	cp /tmp/sqlite-tmp/sqlite-amalgamation-$(SQLITE_VER)/sqlite3.h vendor/sqlite/
	rm -rf /tmp/sqlite.zip /tmp/sqlite-tmp
{% endif %}
# ── Directories ───────────────────────────────────────────
$(BUILD_DIR) $(DIST_DIR):
	mkdir -p $@

# ── Clean ─────────────────────────────────────────────────
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) *.db
