"""The tests for the persistent notification component."""

import pytest

from universalassistant.components import persistent_notification as pn
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


@pytest.fixture(autouse=True)
async def setup_integration(hass: __HAC_KEEP__) -> None:
    """Set up persistent notification integration."""
    assert await async_setup_component(hass, pn.DOMAIN, {})
