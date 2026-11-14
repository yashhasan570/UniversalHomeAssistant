"""AirOS update component for __HA_KEEP__."""

import logging
from typing import Any, override

from airos.exceptions import AirOSConnectionAuthenticationError, AirOSException

from universalassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
    UpdateEntityFeature,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import (
    AirOSConfigEntry,
    AirOSDataUpdateCoordinator,
    AirOSFirmwareUpdateCoordinator,
)
from .entity import AirOSEntity

PARALLEL_UPDATES = 0

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: AirOSConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the AirOS update entity from a config entry."""
    runtime_data = config_entry.runtime_data

    if runtime_data.firmware is None:  # Unsupported device
        return
    async_add_entities([AirOSUpdateEntity(runtime_data.status, runtime_data.firmware)])


class AirOSUpdateEntity(AirOSEntity, UpdateEntity):
    """Update entity for AirOS firmware updates."""

    _attr_device_class = UpdateDeviceClass.FIRMWARE
    _attr_supported_features = UpdateEntityFeature.INSTALL

    def __init__(
        self,
        status: AirOSDataUpdateCoordinator,
        firmware: AirOSFirmwareUpdateCoordinator,
    ) -> None:
        """Initialize the AirOS update entity."""
        super().__init__(status)
        self.status = status
        self.firmware = firmware

        # Legacy format, kept as migrating existing unique IDs is not worth the risk
        self._attr_unique_id = f"{status.data.derived.mac}_firmware_update"  # pylint: disable=universal-assistant-entity-unique-id-redundant-platform

    @property
    @override
    def installed_version(self) -> str | None:
        """Return the installed firmware version."""
        return self.status.data.host.fwversion

    @property
    @override
    def latest_version(self) -> str | None:
        """Return the latest firmware version."""
        if not self.firmware.data.get("update", False):
            return self.status.data.host.fwversion
        return self.firmware.data.get("version")

    @property
    @override
    def release_url(self) -> str | None:
        """Return the release url of the latest firmware."""
        return self.firmware.data.get("changelog")

    @override
    async def async_install(
        self,
        version: str | None,
        backup: bool,
        **kwargs: Any,
    ) -> None:
        """Handle the firmware update installation."""
        _LOGGER.debug("Starting firmware update")
        try:
            await self.status.airos_device.login()
            await self.status.airos_device.download()
            await self.status.airos_device.install()
        except AirOSConnectionAuthenticationError as err:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="update_connection_authentication_error",
            ) from err
        except AirOSException as err:
            raise __HAC_KEEP__Error(
                translation_domain=DOMAIN,
                translation_key="update_error",
            ) from err
