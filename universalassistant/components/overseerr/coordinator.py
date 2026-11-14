"""Define an object to coordinate fetching Overseerr data."""

from datetime import timedelta
from typing import override

from python_overseerr import (
    OverseerrAuthenticationError,
    OverseerrClient,
    OverseerrConnectionError,
)
from yarl import URL

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT, CONF_SSL
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import ConfigEntryAuthFailed
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, LOGGER
from .models import OverseerrData

type OverseerrConfigEntry = ConfigEntry[OverseerrCoordinator]


class OverseerrCoordinator(DataUpdateCoordinator[OverseerrData]):
    """Class to manage fetching Overseerr data."""

    config_entry: OverseerrConfigEntry

    def __init__(self, hass: __HAC_KEEP__, entry: OverseerrConfigEntry) -> None:
        """Initialize."""
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            config_entry=entry,
            update_interval=timedelta(minutes=5),
        )
        host = entry.data[CONF_HOST]
        port = entry.data[CONF_PORT]
        ssl = entry.data[CONF_SSL]
        self.client = OverseerrClient(
            host,
            port,
            entry.data[CONF_API_KEY],
            ssl=ssl,
            session=async_get_clientsession(hass),
        )
        self.url = URL.build(host=host, port=port, scheme="https" if ssl else "http")
        self.push = False

    @override
    async def _async_update_data(self) -> OverseerrData:
        """Fetch data from API endpoint."""
        try:
            requests = await self.client.get_request_count()
            issues = await self.client.get_issue_count()
            return OverseerrData(requests=requests, issues=issues)
        except OverseerrAuthenticationError as err:
            raise ConfigEntryAuthFailed(
                translation_domain=DOMAIN,
                translation_key="auth_error",
            ) from err
        except OverseerrConnectionError as err:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="connection_error",
                translation_placeholders={"error": str(err)},
            ) from err
