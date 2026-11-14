"""The test for the Trafikverket camera platform."""

from datetime import timedelta
from unittest.mock import patch

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import async_fire_time_changed
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker
from pytrafikverket import CameraInfoModel

from universalassistant.components.camera import async_get_image
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error


async def test_camera(
    hass: __HAC_KEEP__,
    load_int: ConfigEntry,
    freezer: FrozenDateTimeFactory,
    monkeypatch: pytest.MonkeyPatch,
    aioclient_mock: AiohttpClientMocker,
    get_camera: CameraInfoModel,
) -> None:
    """Test the Trafikverket Camera sensor."""
    state1 = hass.states.get("camera.test_camera")
    assert state1.state == "idle"
    assert state1.attributes["description"] == "Test Camera for testing"
    assert state1.attributes["location"] == "Test location"
    assert state1.attributes["type"] == "Road"

    with patch(
        "universalassistant.components.trafikverket_camera.coordinator.TrafikverketCamera.async_get_camera",
        return_value=get_camera,
    ):
        aioclient_mock.get(
            "https://www.testurl.com/test_photo.jpg?type=fullsize",
            content=b"9876543210",
        )
        freezer.tick(timedelta(minutes=6))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    state1 = hass.states.get("camera.test_camera")
    assert state1.state == "idle"
    assert state1.attributes != {}

    assert await async_get_image(hass, "camera.test_camera")

    monkeypatch.setattr(
        get_camera,
        "photourl",
        None,
    )
    aioclient_mock.get(
        "https://www.testurl.com/test_photo.jpg?type=fullsize",
        status=404,
    )

    with patch(
        "universalassistant.components.trafikverket_camera.coordinator.TrafikverketCamera.async_get_camera",
        return_value=get_camera,
    ):
        freezer.tick(timedelta(minutes=6))
        async_fire_time_changed(hass)
        await hass.async_block_till_done()

    with pytest.raises(__HAC_KEEP__Error):
        await async_get_image(hass, "camera.test_camera")
