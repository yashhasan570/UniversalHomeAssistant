"""Test the Bluetooth Adapters setup."""

from universalassistant.components.bluetooth_adapters import DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_setup(hass: UniversalAssistant) -> None:
    """Ensure we can setup."""
    assert await async_setup_component(hass, DOMAIN, {})
