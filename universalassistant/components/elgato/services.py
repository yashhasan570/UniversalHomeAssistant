"""Support for Elgato services."""

from enum import StrEnum

from universalassistant.components.light import DOMAIN as LIGHT_DOMAIN
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers import service

from .const import DOMAIN


class ElgatoService(StrEnum):
    """Store keys for Elgato services."""

    IDENTIFY = "identify"


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Set up services."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        ElgatoService.IDENTIFY,
        entity_domain=LIGHT_DOMAIN,
        schema=None,
        func="async_identify",
    )
