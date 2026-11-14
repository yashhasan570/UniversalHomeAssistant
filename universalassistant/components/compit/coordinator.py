"""Define an object to manage fetching Compit data."""

from datetime import timedelta
import logging
from typing import override

from compit_inext_api import CompitApiConnector, DeviceInstance

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=30)
_LOGGER: logging.Logger = logging.getLogger(__name__)

type CompitConfigEntry = ConfigEntry[CompitDataUpdateCoordinator]


class CompitDataUpdateCoordinator(DataUpdateCoordinator[dict[int, DeviceInstance]]):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: __HAC_KEEP__,
        config_entry: CompitConfigEntry,
        connector: CompitApiConnector,
    ) -> None:
        """Initialize."""
        self.connector = connector

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
            config_entry=config_entry,
        )

    @override
    async def _async_update_data(self) -> dict[int, DeviceInstance]:
        """Update data via library."""
        await self.connector.update_state(device_id=None)  # Update all devices
        return self.connector.all_devices
