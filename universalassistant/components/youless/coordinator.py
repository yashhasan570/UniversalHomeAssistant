"""The coordinator for the Youless integration."""

from datetime import timedelta
import logging
from typing import override

from youless_api import YoulessAPI

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

type YouLessConfigEntry = ConfigEntry[YouLessCoordinator]


class YouLessCoordinator(DataUpdateCoordinator[None]):
    """Class to manage fetching YouLess data."""

    config_entry: YouLessConfigEntry

    def __init__(
        self, hass: UniversalAssistant, config_entry: YouLessConfigEntry, device: YoulessAPI
    ) -> None:
        """Initialize global YouLess data provider."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name="youless_gateway",
            update_interval=timedelta(seconds=10),
        )
        self.device = device

    @override
    async def _async_update_data(self) -> None:
        await self.hass.async_add_executor_job(self.device.update)
