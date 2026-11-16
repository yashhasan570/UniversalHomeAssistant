"""The test for the Coolmaster binary sensor platform."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant


async def test_binary_sensor(
    hass: UniversalAssistant,
    load_int: ConfigEntry,
) -> None:
    """Test the Coolmaster binary sensor."""
    assert hass.states.get("binary_sensor.l1_100_clean_filter").state == "off"
    assert hass.states.get("binary_sensor.l1_101_clean_filter").state == "on"
