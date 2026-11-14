"""API for iotty bound to __HA_KEEP__ OAuth."""

from typing import Any, override

from aiohttp import ClientSession
from iottycloud.cloudapi import CloudApi

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_entry_oauth2_flow

OAUTH2_CLIENT_ID = "hass-iotty"
IOTTYAPI_BASE = "https://universalassistant.iotty.com/"


class IottyProxy(CloudApi):
    """Provide iotty authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        hass: __HAC_KEEP__,
        websession: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize iotty auth."""

        super().__init__(websession, IOTTYAPI_BASE, OAUTH2_CLIENT_ID)
        if oauth_session is None:
            raise ValueError("oauth_session")
        self._oauth_session = oauth_session
        self._hass = hass

    @override
    async def async_get_access_token(self) -> Any:
        """Return a valid access token."""
        await self._oauth_session.async_ensure_token_valid()

        return self._oauth_session.token["access_token"]
