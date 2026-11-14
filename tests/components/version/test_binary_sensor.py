"""The test for the version binary sensor platform."""

from universalassistant.components.version.const import DEFAULT_CONFIGURATION
from universalassistant.core import __HAC_KEEP__

from .common import setup_version_integration


async def test_version_binary_sensor_local_source(hass: __HAC_KEEP__) -> None:
    """Test the Version binary sensor with local source."""
    await setup_version_integration(hass)

    state = hass.states.get(
        "binary_sensor.universal_assistant_version_local_installation_update_available"
    )
    assert not state


async def test_version_binary_sensor(hass: __HAC_KEEP__) -> None:
    """Test the Version binary sensor."""
    await setup_version_integration(hass, {**DEFAULT_CONFIGURATION, "source": "pypi"})

    state = hass.states.get(
        "binary_sensor.universal_assistant_version_local_installation_update_available"
    )
    assert state
