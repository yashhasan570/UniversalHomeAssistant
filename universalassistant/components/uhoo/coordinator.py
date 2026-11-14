"""Custom uhoo data update coordinator."""

from typing import override

from uhooapi import Client, Device
from uhooapi.errors import ForbiddenError, UhooError, UnauthorizedError

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, UPDATE_INTERVAL

type UhooConfigEntry = ConfigEntry[UhooDataUpdateCoordinator]


class UhooDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Device]]):
    """Class to manage fetching data from the uHoo API."""

    def __init__(
        self, hass: __HAC_KEEP__, client: Client, entry: UhooConfigEntry
    ) -> None:
        """Initialize DataUpdateCoordinator."""
        self.client = client
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=UPDATE_INTERVAL,
        )

    @override
    async def _async_update_data(self) -> dict[str, Device]:
        try:
            await self.client.login()
            if self.client.devices:
                for device_id in self.client.devices:
                    await self.client.get_latest_data(device_id)
        except (UnauthorizedError, ForbiddenError) as error:
            raise ConfigEntryAuthFailed(f"Invalid API credentials: {error}") from error
        except UhooError as error:
            raise UpdateFailed(f"The device is unavailable: {error}") from error
        else:
            return self.client.devices
