"""The test for the Trafikverket sensor platform."""

import pytest
from pytrafikverket import CameraInfoModel

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: __HAC_KEEP__,
    load_int: ConfigEntry,
    get_camera: CameraInfoModel,
) -> None:
    """Test the Trafikverket Camera sensor."""

    state = hass.states.get("sensor.test_camera_direction")
    assert state.state == "180"
    state = hass.states.get("sensor.test_camera_modified")
    assert state.state == "2022-04-04T04:04:04+00:00"
    state = hass.states.get("sensor.test_camera_photo_time")
    assert state.state == "2022-04-04T04:04:04+00:00"
    state = hass.states.get("sensor.test_camera_photo_url")
    assert state.state == "https://www.testurl.com/test_photo.jpg"
    state = hass.states.get("sensor.test_camera_status")
    assert state.state == "Running"
    state = hass.states.get("sensor.test_camera_camera_type")
    assert state.state == "Road"
