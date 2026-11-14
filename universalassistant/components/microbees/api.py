"""API for microBees bound to __HA_KEEP__ OAuth."""

from universalassistant.const import CONF_ACCESS_TOKEN
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_entry_oauth2_flow


class ConfigEntryAuth:
    """Provide microBees authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        hass: __HAC_KEEP__,
        oauth2_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize microBees Auth."""
        self.oauth_session = oauth2_session
        self.hass = hass

    @property
    def access_token(self) -> str:
        """Return the access token."""
        return self.oauth_session.token[CONF_ACCESS_TOKEN]

    async def check_and_refresh_token(self) -> str:
        """Check the token."""
        await self.oauth_session.async_ensure_token_valid()
        return self.access_token
