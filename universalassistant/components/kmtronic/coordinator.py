"""The kmtronic integration."""

import asyncio
from datetime import timedelta
import logging
from typing import override

from aiohttp.client_exceptions import ClientConnectorError, ClientResponseError
from pykmtronic.hub import KMTronicHubAPI

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import MANUFACTURER

PLATFORMS = [Platform.SWITCH]

_LOGGER = logging.getLogger(__name__)

type KMTronicConfigEntry = ConfigEntry[KMtronicCoordinator]


class KMtronicCoordinator(DataUpdateCoordinator[None]):
    """Coordinator for KMTronic."""

    entry: KMTronicConfigEntry

    def __init__(
        self, hass: __HAC_KEEP__, entry: KMTronicConfigEntry, hub: KMTronicHubAPI
    ) -> None:
        """Initialize the KMTronic coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"{MANUFACTURER} {hub.name}",
            update_interval=timedelta(seconds=30),
        )
        self.hub = hub

    @override
    async def _async_update_data(self) -> None:
        """Fetch the latest data from the source."""
        try:
            async with asyncio.timeout(10):
                await self.hub.async_update_relays()
        except ClientResponseError as err:
            raise UpdateFailed(f"Wrong credentials: {err}") from err
        except ClientConnectorError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
