"""Config flow for SwitchBee Smart Home integration."""

import logging
from typing import Any, override

import probatio
from switchbee.api.central_unit import SwitchBeeError
from switchbee.api.polling import CentralUnitPolling

from universalassistant.config_entries import ConfigFlow, ConfigFlowResult
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.device_registry import format_mac

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = probatio.Schema(
    {
        probatio.Required(CONF_HOST): cv.string,
        probatio.Required(CONF_USERNAME): cv.string,
        probatio.Required(probatio.Secret(CONF_PASSWORD)): cv.string,
    }
)


async def validate_input(hass: __HAC_KEEP__, data: dict[str, Any]) -> str:
    """Validate the user input allows us to connect."""

    websession = async_get_clientsession(hass, verify_ssl=False)
    api = CentralUnitPolling(
        data[CONF_HOST], data[CONF_USERNAME], data[CONF_PASSWORD], websession
    )
    try:
        await api.connect()
    except SwitchBeeError as exp:
        _LOGGER.error(exp)
        if "LOGIN_FAILED" in str(exp):
            raise InvalidAuth from exp

        raise CannotConnect from exp

    if api.unique_id:
        return api.unique_id

    assert api.mac is not None
    return format_mac(api.mac)


class SwitchBeeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SwitchBee Smart Home."""

    VERSION = 2

    @override
    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Show the setup form to the user."""
        errors: dict[str, str] = {}

        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
            )

        try:
            unique_id = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"

        else:
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input[CONF_HOST], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(__HAC_KEEP__Error):
    """Error to indicate we cannot connect."""


class InvalidAuth(__HAC_KEEP__Error):
    """Error to indicate there is invalid auth."""
