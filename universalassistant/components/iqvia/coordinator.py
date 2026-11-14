"""Support for IQVIA."""

from collections.abc import Callable, Coroutine
from datetime import timedelta
from typing import Any, override

from pyiqvia.errors import IQVIAError

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import LOGGER

DEFAULT_SCAN_INTERVAL = timedelta(minutes=30)

type IqviaConfigEntry = ConfigEntry[dict[str, IqviaUpdateCoordinator]]


class IqviaUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Custom DataUpdateCoordinator for IQVIA."""

    config_entry: IqviaConfigEntry

    def __init__(
        self,
        hass: __HAC_KEEP__,
        config_entry: IqviaConfigEntry,
        name: str,
        update_method: Callable[[], Coroutine[Any, Any, dict[str, Any]]],
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            LOGGER,
            name=name,
            config_entry=config_entry,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self._update_method = update_method

    @override
    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the API."""
        try:
            return await self._update_method()
        except IQVIAError as err:
            raise UpdateFailed from err
