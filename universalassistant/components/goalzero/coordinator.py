"""Data update coordinator for the Goal zero integration."""

from datetime import timedelta
from typing import override

from goalzero import Yeti, exceptions

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER

type GoalZeroConfigEntry = ConfigEntry[GoalZeroDataUpdateCoordinator]


class GoalZeroDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Data update coordinator for the Goal zero integration."""

    config_entry: GoalZeroConfigEntry

    def __init__(
        self, hass: UniversalAssistant, config_entry: GoalZeroConfigEntry, api: Yeti
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
        )
        self.api = api

    @override
    async def _async_update_data(self) -> None:
        """Fetch data from API endpoint."""
        try:
            await self.api.get_state()
        except exceptions.ConnectError as err:
            raise UpdateFailed("Failed to communicate with device") from err
