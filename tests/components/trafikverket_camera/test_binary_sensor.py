"""The test for the Trafikverket binary sensor platform."""

import pytest
from pytrafikverket import CameraInfoModel

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import STATE_ON
from universalassistant.core import __HAC_KEEP__


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: __HAC_KEEP__,
    load_int: ConfigEntry,
    get_camera: CameraInfoModel,
) -> None:
    """Test the Trafikverket Camera binary sensor."""

    state = hass.states.get("binary_sensor.test_camera_active")
    assert state.state == STATE_ON
