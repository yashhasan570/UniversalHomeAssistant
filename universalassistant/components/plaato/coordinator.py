"""Coordinator for Plaato devices."""

from dataclasses import dataclass, field
from datetime import timedelta
import logging
from typing import override

from pyplaato.models.device import PlaatoDevice
from pyplaato.plaato import Plaato, PlaatoDeviceType

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import aiohttp_client
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


@dataclass
class PlaatoData:
    """Runtime data for the Plaato integration."""

    coordinator: PlaatoCoordinator | None
    device_name: str
    device_type: str
    device_id: str | None
    sensor_data: PlaatoDevice | None = field(default=None)


type PlaatoConfigEntry = ConfigEntry[PlaatoData]


class PlaatoCoordinator(DataUpdateCoordinator[PlaatoDevice]):
    """Class to manage fetching data from the API."""

    config_entry: PlaatoConfigEntry

    def __init__(
        self,
        hass: __HAC_KEEP__,
        config_entry: PlaatoConfigEntry,
        auth_token: str,
        device_type: PlaatoDeviceType,
    ) -> None:
        """Initialize."""
        self.api = Plaato(auth_token=auth_token)
        self.device_type = device_type
        self.platforms: list[Platform] = []

        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(minutes=SCAN_INTERVAL),
        )

    @override
    async def _async_update_data(self) -> PlaatoDevice:
        """Update data via library."""
        return await self.api.get_data(
            session=aiohttp_client.async_get_clientsession(self.hass),
            device_type=self.device_type,
        )
