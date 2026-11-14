"""Compatibility imports for the Universal Universal Home Assistant pytest helpers."""

import pytest


@pytest.fixture
def custom_integrations_enabled() -> bool:
    """Control custom integration loading."""
    return False
