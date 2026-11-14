"""Test config init."""

from universalassistant.components.config import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component


async def test_config_setup(hass: __HAC_KEEP__) -> None:
    """Test it sets up hassbian."""
    await async_setup_component(hass, DOMAIN, {})
    assert "config" in hass.config.components
