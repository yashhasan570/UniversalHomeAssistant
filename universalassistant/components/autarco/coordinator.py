"""Coordinator for Autarco integration."""

from typing import NamedTuple, override

from autarco import (
    AccountSite,
    Autarco,
    AutarcoAuthenticationError,
    AutarcoConnectionError,
    Battery,
    Inverter,
    Site,
    Solar,
)

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER, SCAN_INTERVAL

type AutarcoConfigEntry = ConfigEntry[list[AutarcoDataUpdateCoordinator]]


class AutarcoData(NamedTuple):
    """Class for defining data in dict."""

    solar: Solar
    inverters: dict[str, Inverter]
    site: Site
    battery: Battery | None


class AutarcoDataUpdateCoordinator(DataUpdateCoordinator[AutarcoData]):
    """Class to manage fetching Autarco data from the API."""

    config_entry: AutarcoConfigEntry

    def __init__(
        self,
        hass: __HAC_KEEP__,
        config_entry: AutarcoConfigEntry,
        client: Autarco,
        account_site: AccountSite,
    ) -> None:
        """Initialize global Autarco data updater."""
        super().__init__(
            hass,
            LOGGER,
            config_entry=config_entry,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )
        self.client = client
        self.account_site = account_site

    @override
    async def _async_update_data(self) -> AutarcoData:
        """Fetch data from Autarco API."""
        battery = None
        try:
            site = await self.client.get_site(self.account_site.public_key)
            solar = await self.client.get_solar(self.account_site.public_key)
            inverters = await self.client.get_inverters(self.account_site.public_key)
            if site.has_battery:
                battery = await self.client.get_battery(self.account_site.public_key)
        except AutarcoAuthenticationError as err:
            raise ConfigEntryAuthFailed(err) from err
        except AutarcoConnectionError as err:
            raise UpdateFailed(err) from err
        return AutarcoData(
            solar=solar,
            inverters=inverters,
            site=site,
            battery=battery,
        )
