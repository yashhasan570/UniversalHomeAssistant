"""Coordinator for the Garages Amsterdam integration."""

from typing import override

from odp_amsterdam import Garage, ODPAmsterdam, VehicleType

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER, SCAN_INTERVAL

type GaragesAmsterdamConfigEntry = ConfigEntry[GaragesAmsterdamDataUpdateCoordinator]


class GaragesAmsterdamDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Garage]]):
    """Class to manage fetching Garages Amsterdam data from single endpoint."""

    config_entry: GaragesAmsterdamConfigEntry

    def __init__(
        self,
        hass: UniversalAssistant,
        config_entry: GaragesAmsterdamConfigEntry,
        client: ODPAmsterdam,
    ) -> None:
        """Initialize global Garages Amsterdam data updater."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.client = client

    @override
    async def _async_update_data(self) -> dict[str, Garage]:
        return {
            garage.garage_name: garage
            for garage in await self.client.all_garages(vehicle=VehicleType.CAR)
        }
