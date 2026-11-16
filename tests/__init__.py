"""Tests for Universal Home Assistant."""

from pathlib import Path

from pytest_universalassistant import _paths

# Alias httpx to httpx2 before any test module or fixture imports httpx
import universalassistant  # noqa: F401

_paths.TESTS_DIR = Path(__file__).parent
_paths.CONFIG_DIR = _paths.TESTS_DIR / "testing_config"
