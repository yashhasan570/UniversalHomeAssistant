"""Services for the input_button integration."""

import probatio

from universalassistant.const import CONF_ID
from universalassistant.core import __HAC_KEEP__, ServiceCall, callback
from universalassistant.helpers.service import async_register_admin_service

from .const import DATA_INPUT_BUTTON, DOMAIN, InputButtonService

RELOAD_SERVICE_SCHEMA = probatio.Schema({})


async def _async_reload_service(service_call: ServiceCall) -> None:
    """Remove all input buttons and load new ones from config."""
    hass = service_call.hass
    data = hass.data[DATA_INPUT_BUTTON]
    conf = await data.component.async_prepare_reload(skip_reset=True)
    await data.yaml_collection.async_load(
        [{CONF_ID: id_, **(conf or {})} for id_, conf in conf.get(DOMAIN, {}).items()]
    )


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Register the input_button services."""
    async_register_admin_service(
        hass,
        DOMAIN,
        InputButtonService.RELOAD,
        _async_reload_service,
        schema=RELOAD_SERVICE_SCHEMA,
    )

    hass.data[DATA_INPUT_BUTTON].component.async_register_entity_service(
        InputButtonService.PRESS, None, "_async_press_action"
    )
