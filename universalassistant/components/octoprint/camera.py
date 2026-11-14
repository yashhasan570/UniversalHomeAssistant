"""Support for OctoPrint binary camera."""

from pyoctoprintapi import WebcamSettings

from universalassistant.components.mjpeg import MjpegCamera
from universalassistant.const import CONF_VERIFY_SSL
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import OctoprintConfigEntry, OctoprintDataUpdateCoordinator


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: OctoprintConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the available OctoPrint camera."""
    coordinator = config_entry.runtime_data
    client = coordinator.octoprint
    device_id = config_entry.unique_id

    assert device_id is not None

    camera_info = await client.get_webcam_info()
    verify_ssl = config_entry.data[CONF_VERIFY_SSL]

    if not camera_info or not camera_info.enabled:
        return

    async_add_entities(
        [
            OctoprintCamera(
                camera_info,
                coordinator,
                device_id,
                verify_ssl,
            )
        ]
    )


class OctoprintCamera(CoordinatorEntity[OctoprintDataUpdateCoordinator], MjpegCamera):
    """Representation of an OctoPrint Camera Stream."""

    def __init__(
        self,
        camera_settings: WebcamSettings,
        coordinator: OctoprintDataUpdateCoordinator,
        device_id: str,
        verify_ssl: bool,
    ) -> None:
        """Initialize as a subclass of MjpegCamera."""
        super().__init__(
            coordinator=coordinator,
        )
        MjpegCamera.__init__(
            self,
            device_info=coordinator.device_info,
            mjpeg_url=camera_settings.stream_url,
            name="OctoPrint Camera",
            still_image_url=camera_settings.external_snapshot_url,
            unique_id=device_id,
            verify_ssl=verify_ssl,
        )
