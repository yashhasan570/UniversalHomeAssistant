"""The Aurora integration."""

from datetime import timedelta
import logging
from typing import override

from aiohttp import ClientError
from auroranoaa import AuroraForecast

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_THRESHOLD, DEFAULT_THRESHOLD

_LOGGER = logging.getLogger(__name__)

type AuroraConfigEntry = ConfigEntry[AuroraDataUpdateCoordinator]


class AuroraDataUpdateCoordinator(DataUpdateCoordinator[int]):
    """Class to manage fetching data from the NOAA Aurora API."""

    config_entry: AuroraConfigEntry

    def __init__(self, hass: UniversalAssistant, config_entry: AuroraConfigEntry) -> None:
        """Initialize the data updater."""

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            config_entry=config_entry,
            name="Aurora",
            update_interval=timedelta(minutes=5),
        )

        self.api = AuroraForecast(async_get_clientsession(hass))
        self.latitude = round(self.config_entry.data[CONF_LATITUDE])
        self.longitude = round(self.config_entry.data[CONF_LONGITUDE])
        self.threshold = int(
            self.config_entry.options.get(CONF_THRESHOLD, DEFAULT_THRESHOLD)
        )

    @override
    async def _async_update_data(self) -> int:
        """Fetch the data from the NOAA Aurora Forecast."""

        try:
            return await self.api.get_forecast_data(self.longitude, self.latitude)
        except ClientError as error:
            raise UpdateFailed(f"Error updating from NOAA: {error}") from error
