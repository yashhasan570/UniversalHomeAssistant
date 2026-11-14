"""Helpers to help coordinate updates."""

from typing import override

from pypalazzetti.client import PalazzettiClient
from pypalazzetti.exceptions import CommunicationError, ValidationError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL

type PalazzettiConfigEntry = ConfigEntry[PalazzettiDataUpdateCoordinator]


class PalazzettiDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching Palazzetti data from a Palazzetti hub."""

    config_entry: PalazzettiConfigEntry
    client: PalazzettiClient

    def __init__(
        self,
        hass: __HAC_KEEP__,
        config_entry: PalazzettiConfigEntry,
    ) -> None:
        """Initialize global Palazzetti data updater."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.client = PalazzettiClient(
            self.config_entry.data[CONF_HOST],
            session=async_get_clientsession(hass),
        )

    @override
    async def _async_setup(self) -> None:
        try:
            await self.client.connect()
            await self.client.update_state()
        except (CommunicationError, ValidationError) as err:
            raise UpdateFailed(f"Error communicating with the API: {err}") from err

    @override
    async def _async_update_data(self) -> None:
        """Fetch data from Palazzetti."""
        try:
            await self.client.update_state()
        except (CommunicationError, ValidationError) as err:
            raise UpdateFailed(f"Error communicating with the API: {err}") from err
