"""The test for the Coolmaster binary sensor platform."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__


async def test_binary_sensor(
    hass: __HAC_KEEP__,
    load_int: ConfigEntry,
) -> None:
    """Test the Coolmaster binary sensor."""
    assert hass.states.get("binary_sensor.l1_100_clean_filter").state == "off"
    assert hass.states.get("binary_sensor.l1_101_clean_filter").state == "on"
