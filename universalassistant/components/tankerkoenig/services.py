"""Services for the Tankerkoenig integration."""

from enum import StrEnum

from universalassistant.components.binary_sensor import DOMAIN as BINARY_SENSOR_DOMAIN
from universalassistant.core import UniversalAssistant, SupportsResponse, callback
from universalassistant.helpers import service

from .const import DOMAIN


class TankerkoenigService(StrEnum):
    """Store keys for Tankerkoenig services."""

    GET_OPENING_TIMES = "get_opening_times"


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Set up the services for the Tankerkoenig integration."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        TankerkoenigService.GET_OPENING_TIMES,
        entity_domain=BINARY_SENSOR_DOMAIN,
        schema=None,
        func="async_get_opening_times",
        supports_response=SupportsResponse.ONLY,
    )
