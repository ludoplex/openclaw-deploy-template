#!/bin/bash
# Fetch vendor dependencies for {{ cookiecutter.project_name }}
set -euo pipefail

COSMOCC_VER="${COSMOCC_VER:-3.9.7}"
SQLITE_VER="3480000"

mkdir -p vendor

# cosmocc
if [ ! -d "cosmocc" ]; then
    echo "Downloading cosmocc ${COSMOCC_VER}..."
    curl -L "https://cosmo.zip/pub/cosmocc/cosmocc-${COSMOCC_VER}.zip" -o /tmp/cosmocc.zip
    unzip -q /tmp/cosmocc.zip -d cosmocc
    rm /tmp/cosmocc.zip
    echo "cosmocc ready at ./cosmocc/bin/"
else
    echo "cosmocc already present"
fi

{% if cookiecutter.use_sqlite == "yes" %}
# SQLite amalgamation
if [ ! -f "vendor/sqlite/sqlite3.c" ]; then
    echo "Downloading SQLite amalgamation..."
    mkdir -p vendor/sqlite
    curl -L "https://www.sqlite.org/2025/sqlite-amalgamation-${SQLITE_VER}.zip" -o /tmp/sqlite.zip
    unzip -o /tmp/sqlite.zip -d /tmp/sqlite-tmp
    cp /tmp/sqlite-tmp/sqlite-amalgamation-${SQLITE_VER}/sqlite3.c vendor/sqlite/
    cp /tmp/sqlite-tmp/sqlite-amalgamation-${SQLITE_VER}/sqlite3.h vendor/sqlite/
    rm -rf /tmp/sqlite.zip /tmp/sqlite-tmp
    echo "SQLite amalgamation ready"
else
    echo "SQLite amalgamation already present"
fi
{% endif %}

echo "Vendor setup complete"
