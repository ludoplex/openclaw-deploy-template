"""
Pytest configuration and shared fixtures for SOP Dashboard tests.
"""

import pytest
import sys
from pathlib import Path

# Ensure workspace is in path for imports
WORKSPACE = Path(__file__).parent.parent
sys.path.insert(0, str(WORKSPACE))


@pytest.fixture(scope="session")
def workspace_path():
    """Return the workspace path."""
    return WORKSPACE


@pytest.fixture(scope="session")
def sops_path(workspace_path):
    """Return the SOPs directory path."""
    return workspace_path / "sops"


@pytest.fixture(scope="session")
def templates_path(workspace_path):
    """Return the templates directory path."""
    return workspace_path / "src" / "dashboard" / "templates"
