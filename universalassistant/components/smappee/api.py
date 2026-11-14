"""API for Smappee bound to __HA_KEEP__ OAuth."""

from asyncio import run_coroutine_threadsafe
from typing import TYPE_CHECKING

from pysmappee import api

from universalassistant import core
from universalassistant.const import CONF_PLATFORM
from universalassistant.helpers import config_entry_oauth2_flow

from .const import DOMAIN

if TYPE_CHECKING:
    from . import SmappeeConfigEntry


class ConfigEntrySmappeeApi(api.SmappeeApi):
    """Provide Smappee authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        hass: core.__HAC_KEEP__,
        config_entry: SmappeeConfigEntry,
        session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize Smappee Auth."""
        self.hass = hass
        self.config_entry = config_entry
        self.session = session

        platform_to_farm = {
            "PRODUCTION": 1,
            "ACCEPTANCE": 2,
            "DEVELOPMENT": 3,
        }
        super().__init__(
            None,
            None,
            token=self.session.token,
            # Uses legacy hass.data[DOMAIN] pattern
            # pylint: disable-next=universal-assistant-use-runtime-data
            farm=platform_to_farm[hass.data[DOMAIN][CONF_PLATFORM]],
        )

    def refresh_tokens(self) -> dict:
        """Refresh and return new Smappee tokens using __HA_KEEP__ OAuth2 session."""
        run_coroutine_threadsafe(
            self.session.async_ensure_token_valid(), self.hass.loop
        ).result()

        return self.session.token
