"""Data update coordinator for the Skybell integration."""

from datetime import timedelta
from typing import override

from aioskybell import SkybellDevice, SkybellException

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import LOGGER

type SkybellConfigEntry = ConfigEntry[list[SkybellDataUpdateCoordinator]]


class SkybellDataUpdateCoordinator(DataUpdateCoordinator[None]):
    """Data update coordinator for the Skybell integration."""

    config_entry: SkybellConfigEntry

    def __init__(
        self,
        hass: __HAC_KEEP__,
        config_entry: SkybellConfigEntry,
        device: SkybellDevice,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            config_entry=config_entry,
            name=device.name,
            update_interval=timedelta(seconds=30),
        )
        self.device = device

    @override
    async def _async_update_data(self) -> None:
        """Fetch data from API endpoint."""
        try:
            await self.device.async_update()
        except SkybellException as err:
            raise UpdateFailed(f"Failed to communicate with device: {err}") from err
