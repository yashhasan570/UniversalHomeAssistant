"""Tests for the Recovery Mode integration."""

from pytest_universalassistant.common import async_get_persistent_notifications

from universalassistant.components.recovery_mode import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


async def test_works(hass: __HAC_KEEP__) -> None:
    """Test Recovery Mode works."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    notifications = async_get_persistent_notifications(hass)
    assert len(notifications) == 1
