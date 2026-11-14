"""Coordinator for Vallox ventilation units."""

import logging
from typing import override

from vallox_websocket_api import MetricData, Vallox, ValloxApiException

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_NAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import STATE_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

type ValloxConfigEntry = ConfigEntry[ValloxDataUpdateCoordinator]


class ValloxDataUpdateCoordinator(DataUpdateCoordinator[MetricData]):
    """The DataUpdateCoordinator for Vallox."""

    config_entry: ValloxConfigEntry

    def __init__(
        self,
        hass: __HAC_KEEP__,
        config_entry: ValloxConfigEntry,
        client: Vallox,
    ) -> None:
        """Initialize Vallox data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=config_entry,
            name=f"{config_entry.data[CONF_NAME]} DataUpdateCoordinator",
            update_interval=STATE_SCAN_INTERVAL,
        )
        self.client = client

    @override
    async def _async_update_data(self) -> MetricData:
        """Fetch state update."""
        _LOGGER.debug("Updating Vallox state cache")

        try:
            return await self.client.fetch_metric_data()
        except ValloxApiException as err:
            raise UpdateFailed("Error during state cache update") from err
