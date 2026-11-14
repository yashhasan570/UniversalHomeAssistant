"""Coordinator for the Dexcom integration."""

from datetime import timedelta
import logging
from typing import override

from pydexcom import Dexcom, GlucoseReading

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

_SCAN_INTERVAL = timedelta(seconds=180)

type DexcomConfigEntry = ConfigEntry[DexcomCoordinator]


class DexcomCoordinator(DataUpdateCoordinator[GlucoseReading | None]):
    """Dexcom Coordinator."""

    def __init__(
        self,
        hass: __HAC_KEEP__,
        entry: DexcomConfigEntry,
        dexcom: Dexcom,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=_SCAN_INTERVAL,
        )
        self.dexcom = dexcom

    @override
    async def _async_update_data(self) -> GlucoseReading | None:
        """Fetch data from API endpoint."""
        return await self.hass.async_add_executor_job(
            self.dexcom.get_current_glucose_reading
        )
