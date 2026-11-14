"""Config flow for Roth Touchline integration."""

import logging
from typing import Any, override

import probatio
from pytouchline_extended import PyTouchline

from universalassistant.config_entries import ConfigFlow, ConfigFlowResult
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = probatio.Schema(
    {
        probatio.Required(CONF_HOST): cv.string,
    }
)


def fetch_unique_id(host: str) -> str:
    """Fetch the unique id for the Touchline controller."""
    client = PyTouchline(url=host)
    client.get_number_of_devices()
    client.update()
    return str(client.get_controller_id())


async def _async_validate_input(hass: __HAC_KEEP__, data: dict[str, Any]) -> str:
    """Validate the user input allows us to connect."""
    host = data[CONF_HOST]

    try:
        return await hass.async_add_executor_job(fetch_unique_id, host)
    except (OSError, ConnectionError, TimeoutError) as err:
        _LOGGER.debug(
            "Error while connecting to Touchline controller at %s", host, exc_info=True
        )
        raise CannotConnect from err


class CannotConnect(__HAC_KEEP__Error):
    """Error to indicate we cannot connect."""


class TouchlineConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Roth Touchline."""

    VERSION = 1

    @override
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})

            try:
                unique_id = await _async_validate_input(self.hass, user_input)

            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            if not errors:
                await self.async_set_unique_id(unique_id)
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input[CONF_HOST], data=user_input
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
