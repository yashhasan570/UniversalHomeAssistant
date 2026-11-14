"""Coordinator for Iskra integration."""

from datetime import timedelta
import logging
from typing import override

from pyiskra.devices import Device
from pyiskra.exceptions import (
    DeviceConnectionError,
    DeviceTimeoutError,
    InvalidResponseCode,
    NotAuthorised,
)

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

type IskraConfigEntry = ConfigEntry[list[IskraDataUpdateCoordinator]]


class IskraDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching Iskra data."""

    config_entry: IskraConfigEntry

    def __init__(
        self, hass: __HAC_KEEP__, config_entry: IskraConfigEntry, device: Device
    ) -> None:
        """Initialize."""
        self.device = device

        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )

    @override
    async def _async_update_data(self) -> None:
        """Fetch data from Iskra device."""
        try:
            await self.device.update_status()
        except DeviceTimeoutError as e:
            raise UpdateFailed(
                "Timeout error occurred while updating"
                f" data for device {self.device.serial}"
            ) from e
        except DeviceConnectionError as e:
            raise UpdateFailed(
                "Connection error occurred while updating"
                f" data for device {self.device.serial}"
            ) from e
        except NotAuthorised as e:
            raise UpdateFailed(
                f"Not authorised to fetch data from device {self.device.serial}"
            ) from e
        except InvalidResponseCode as e:
            raise UpdateFailed(
                f"Invalid response code from device {self.device.serial}"
            ) from e
