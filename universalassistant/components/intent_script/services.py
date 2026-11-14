"""Services for the intent_script integration."""

from enum import StrEnum

from universalassistant.core import UniversalAssistant, ServiceCall, callback
from universalassistant.helpers.service import async_register_admin_service

from .const import DOMAIN
from .helpers import async_reload


class IntentScriptService(StrEnum):
    """Store keys for Intent Script services."""

    RELOAD = "reload"


async def _handle_reload(service_call: ServiceCall) -> None:
    return await async_reload(service_call.hass, service_call)


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Set up the services for the intent_script integration."""
    async_register_admin_service(
        hass,
        DOMAIN,
        IntentScriptService.RELOAD,
        _handle_reload,
    )
