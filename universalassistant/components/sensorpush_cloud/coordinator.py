"""Coordinator for the SensorPush Cloud integration."""

from typing import override

from sensorpush_ha import (
    SensorPushCloudApi,
    SensorPushCloudData,
    SensorPushCloudError,
    SensorPushCloudHelper,
)

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_EMAIL, CONF_PASSWORD
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import LOGGER, UPDATE_INTERVAL

type SensorPushCloudConfigEntry = ConfigEntry[SensorPushCloudCoordinator]


class SensorPushCloudCoordinator(DataUpdateCoordinator[dict[str, SensorPushCloudData]]):
    """SensorPush Cloud coordinator."""

    def __init__(self, hass: __HAC_KEEP__, entry: SensorPushCloudConfigEntry) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=entry.title,
            update_interval=UPDATE_INTERVAL,
            config_entry=entry,
        )
        email, password = entry.data[CONF_EMAIL], entry.data[CONF_PASSWORD]
        clientsession = async_get_clientsession(hass)
        api = SensorPushCloudApi(email, password, clientsession)
        self.helper = SensorPushCloudHelper(api)

    @override
    async def _async_update_data(self) -> dict[str, SensorPushCloudData]:
        """Fetch data from API endpoints."""
        try:
            return await self.helper.async_get_data()
        except SensorPushCloudError as e:
            raise UpdateFailed(e) from e
