"""The test for the Trafikverket binary sensor platform."""

import pytest
from pytrafikverket import CameraInfoModel

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import STATE_ON
from universalassistant.core import UniversalAssistant


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: UniversalAssistant,
    load_int: ConfigEntry,
    get_camera: CameraInfoModel,
) -> None:
    """Test the Trafikverket Camera binary sensor."""

    state = hass.states.get("binary_sensor.test_camera_active")
    assert state.state == STATE_ON
