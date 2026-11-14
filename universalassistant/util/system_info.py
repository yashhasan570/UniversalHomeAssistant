"""Util to gather system info."""

from functools import cache
import os


@cache
def is_official_image() -> bool:
    """Return True if __HA_KEEP__ is running in an official container."""
    return os.path.isfile("/OFFICIAL_IMAGE")
