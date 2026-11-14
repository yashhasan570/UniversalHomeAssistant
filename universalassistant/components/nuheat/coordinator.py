"""DataUpdateCoordinator for NuHeat thermostats."""

from datetime import timedelta
import logging
from typing import override

import nuheat

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import CONF_SERIAL_NUMBER

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


type NuHeatConfigEntry = ConfigEntry[NuHeatCoordinator]


class NuHeatCoordinator(DataUpdateCoordinator[None]):
    """Coordinator for NuHeat thermostat data."""

    config_entry: NuHeatConfigEntry

    def __init__(
        self,
        hass: __HAC_KEEP__,
        entry: NuHeatConfigEntry,
        thermostat: nuheat.NuHeatThermostat,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=f"nuheat {entry.data[CONF_SERIAL_NUMBER]}",
            update_interval=SCAN_INTERVAL,
        )
        self.thermostat = thermostat

    @override
    async def _async_update_data(self) -> None:
        """Fetch data from API endpoint."""
        await self.hass.async_add_executor_job(self.thermostat.get_data)
