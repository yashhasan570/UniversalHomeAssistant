"""DataUpdateCoordinator for poolsense integration."""

import asyncio
from datetime import timedelta
import logging
from typing import override

from poolsense import PoolSense
from poolsense.exceptions import PoolSenseError

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_EMAIL
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.typing import StateType
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

type PoolSenseConfigEntry = ConfigEntry[PoolSenseDataUpdateCoordinator]


class PoolSenseDataUpdateCoordinator(DataUpdateCoordinator[dict[str, StateType]]):
    """Define an object to hold PoolSense data."""

    config_entry: PoolSenseConfigEntry

    def __init__(
        self,
        hass: __HAC_KEEP__,
        config_entry: PoolSenseConfigEntry,
        poolsense: PoolSense,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=timedelta(hours=1),
        )
        self.poolsense = poolsense
        self.email = self.config_entry.data[CONF_EMAIL]

    @override
    async def _async_update_data(self) -> dict[str, StateType]:
        """Update data via library."""
        async with asyncio.timeout(10):
            try:
                return await self.poolsense.get_poolsense_data()
            except PoolSenseError as error:
                raise UpdateFailed(
                    f"PoolSense query did not complete: {error}"
                ) from error
