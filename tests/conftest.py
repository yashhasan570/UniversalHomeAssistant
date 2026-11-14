"""Compatibility imports for the __HA_KEEP__ pytest helpers."""

import pytest


@pytest.fixture
def custom_integrations_enabled() -> bool:
    """Control custom integration loading."""
    return False
