"""Config flow for Universal Home Assistant Supervisor integration."""

from typing import Any

from universalassistant.components.http.const import DATA_SUPERVISOR_USER
from universalassistant.config_entries import ConfigFlow, ConfigFlowResult
from universalassistant.const import HASSIO_USER_NAME

from .const import DEFAULT_UPDATE_OPTIONS, DOMAIN, ENTRY_DATA_USER


class HassIoConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Universal Home Assistant Supervisor."""

    VERSION = 1

    async def async_step_system(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        data: dict[str, Any] = {}
        if (user := self.hass.data.get(DATA_SUPERVISOR_USER)) is not None:
            data[ENTRY_DATA_USER] = user.id

        return self.async_create_entry(
            title=HASSIO_USER_NAME,
            data=data,
            options=dict(DEFAULT_UPDATE_OPTIONS),
        )
