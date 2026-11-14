"""Provides the Geocaching DataUpdateCoordinator."""

from typing import override

from geocachingapi.exceptions import GeocachingApiError, GeocachingInvalidSettingsError
from geocachingapi.geocachingapi import GeocachingApi
from geocachingapi.models import GeocachingStatus

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.config_entry_oauth2_flow import OAuth2Session
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, ENVIRONMENT, LOGGER, UPDATE_INTERVAL

type GeocachingConfigEntry = ConfigEntry[GeocachingDataUpdateCoordinator]


class GeocachingDataUpdateCoordinator(DataUpdateCoordinator[GeocachingStatus]):
    """Class to manage fetching Geocaching data from single endpoint."""

    config_entry: GeocachingConfigEntry

    def __init__(
        self,
        hass: __HAC_KEEP__,
        *,
        entry: GeocachingConfigEntry,
        session: OAuth2Session,
    ) -> None:
        """Initialize global Geocaching data updater."""
        self.session = session

        async def async_token_refresh() -> str:
            await session.async_ensure_token_valid()
            token = session.token["access_token"]
            LOGGER.debug(str(token))
            return str(token)

        client_session = async_get_clientsession(hass)

        self.geocaching = GeocachingApi(
            environment=ENVIRONMENT,
            token=session.token["access_token"],
            session=client_session,
            token_refresh_method=async_token_refresh,
        )

        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )

    @override
    async def _async_update_data(self) -> GeocachingStatus:
        """Fetch the latest Geocaching status."""
        try:
            return await self.geocaching.update()
        except GeocachingInvalidSettingsError as error:
            raise UpdateFailed(f"Invalid integration configuration: {error}") from error
        except GeocachingApiError as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error
