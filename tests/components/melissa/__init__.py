"""Tests for the melissa component."""

from universalassistant.components.melissa import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

VALID_CONFIG = {"melissa": {"username": "********", "password": "********"}}


async def setup_integration(hass: UniversalAssistant) -> None:
    """Set up the melissa integration in Universal Home Assistant."""
    assert await async_setup_component(hass, DOMAIN, VALID_CONFIG)
    await hass.async_block_till_done()
