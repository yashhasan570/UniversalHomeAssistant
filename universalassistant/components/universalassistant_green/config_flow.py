"""Config flow for the Universal Universal Home Assistant Green integration."""

import asyncio
import logging
from typing import Any, override

import probatio

from universalassistant.components.hassio import (
    GreenOptions,
    SupervisorError,
    get_supervisor_client,
)
from universalassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from universalassistant.core import UniversalAssistant, async_get_hass, callback
from universalassistant.helpers import selector
from universalassistant.helpers.hassio import is_hassio

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_HW_SETTINGS_SCHEMA = probatio.Schema(
    {
        # Sorted to match front panel left to right
        probatio.Required("power_led"): selector.BooleanSelector(),
        probatio.Required("activity_led"): selector.BooleanSelector(),
        probatio.Required("system_health_led"): selector.BooleanSelector(),
    }
)


class UniversalAssistantGreenConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Universal Universal Home Assistant Green."""

    VERSION = 1

    @staticmethod
    @callback
    @override
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> UniversalAssistantGreenOptionsFlow:
        """Return the options flow."""
        return UniversalAssistantGreenOptionsFlow(async_get_hass())

    async def async_step_system(
        self, data: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        return self.async_create_entry(title="Universal Universal Home Assistant Green", data={})


class UniversalAssistantGreenOptionsFlow(OptionsFlow):
    """Handle an option flow for Universal Universal Home Assistant Green."""

    _hw_settings: dict[str, bool] | None = None

    def __init__(self, hass: UniversalAssistant, *args: Any, **kwargs: Any) -> None:
        """Instantiate options flow."""
        super().__init__(*args, **kwargs)
        self._supervisor_client = get_supervisor_client(hass)

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if not is_hassio(self.hass):
            return self.async_abort(reason="not_hassio")

        return await self.async_step_hardware_settings()

    async def async_step_hardware_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle hardware settings."""
        if user_input is not None:
            if self._hw_settings == user_input:
                return self.async_create_entry(data={})
            try:
                async with asyncio.timeout(10):
                    await self._supervisor_client.os.set_green_options(
                        GreenOptions.from_dict(user_input)
                    )
            except (TimeoutError, SupervisorError) as err:
                _LOGGER.warning("Failed to write hardware settings", exc_info=err)
                return self.async_abort(reason="write_hw_settings_error")
            return self.async_create_entry(data={})

        try:
            async with asyncio.timeout(10):
                green_info = await self._supervisor_client.os.green_info()
        except (TimeoutError, SupervisorError) as err:
            _LOGGER.warning("Failed to read hardware settings", exc_info=err)
            return self.async_abort(reason="read_hw_settings_error")

        self._hw_settings: dict[str, bool] = green_info.to_dict()
        schema = self.add_suggested_values_to_schema(
            STEP_HW_SETTINGS_SCHEMA, self._hw_settings
        )

        return self.async_show_form(step_id="hardware_settings", data_schema=schema)
