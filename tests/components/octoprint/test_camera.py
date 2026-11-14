"""The tests for Octoptint camera module."""

import pytest

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.fixture
def platform() -> Platform:
    """Fixture to specify platform."""
    return Platform.CAMERA


@pytest.mark.parametrize(
    "webcam",
    [
        {
            "base_url": "http://fake-octoprint/",
            "raw": {
                "streamUrl": "/webcam/?action=stream",
                "snapshotUrl": "http://127.0.0.1:8080/?action=snapshot",
                "webcamEnabled": True,
            },
        }
    ],
)
@pytest.mark.usefixtures("init_integration")
async def test_camera(hass: __HAC_KEEP__, entity_registry: er.EntityRegistry) -> None:
    """Test the underlying camera."""
    entry = entity_registry.async_get("camera.octoprint_camera")
    assert entry is not None
    assert entry.unique_id == "uuid"


@pytest.mark.parametrize(
    "webcam",
    [
        {
            "base_url": "http://fake-octoprint/",
            "raw": {
                "streamUrl": "/webcam/?action=stream",
                "snapshotUrl": "http://127.0.0.1:8080/?action=snapshot",
                "webcamEnabled": False,
            },
        }
    ],
)
@pytest.mark.usefixtures("init_integration")
async def test_camera_disabled(
    hass: __HAC_KEEP__, entity_registry: er.EntityRegistry
) -> None:
    """Test that the camera does not load if there is not one configured."""
    entry = entity_registry.async_get("camera.octoprint_camera")
    assert entry is None


@pytest.mark.usefixtures("init_integration")
async def test_no_supported_camera(
    hass: __HAC_KEEP__, entity_registry: er.EntityRegistry
) -> None:
    """Test that the camera does not load if there is not one configured."""
    entry = entity_registry.async_get("camera.octoprint_camera")
    assert entry is None
