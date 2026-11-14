"""Test the Intelligent Storage Acceleration setup."""

from universalassistant.components.isal import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_setup(hass: UniversalAssistant) -> None:
    """Ensure we can setup."""
    assert await async_setup_component(hass, DOMAIN, {})
