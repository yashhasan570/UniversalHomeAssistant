"""Services for the rest integration."""

import contextlib
from enum import StrEnum

import probatio

from universalassistant.core import __HAC_KEEP__, ServiceCall, callback
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.reload import (
    async_integration_yaml_config,
    async_reload_integration_platforms,
)

from .const import DOMAIN, PLATFORMS
from .util import async_process_config, async_setup_shared_data


class RestService(StrEnum):
    """Store keys for RESTful services."""

    RELOAD = "reload"


async def _reload_service_handler(service: ServiceCall) -> None:
    """Remove all user-defined groups and load new ones from config."""
    hass = service.hass
    conf = None
    # pylint: disable-next=universal-assistant-action-swallowed-exception
    with contextlib.suppress(__HAC_KEEP__Error):
        conf = await async_integration_yaml_config(hass, DOMAIN)
    if conf is None:
        return
    await async_reload_integration_platforms(hass, DOMAIN, PLATFORMS)
    async_setup_shared_data(hass)
    await async_process_config(hass, conf)


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Register the rest services."""
    hass.services.async_register(
        DOMAIN, RestService.RELOAD, _reload_service_handler, schema=probatio.Schema({})
    )
