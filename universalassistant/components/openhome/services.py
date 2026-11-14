"""Support for Openhome Devices."""

import probatio

from universalassistant.components.media_player import DOMAIN as MEDIA_PLAYER_DOMAIN
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers import config_validation as cv, service

from .const import DOMAIN, OpenhomeService, OpenhomeServiceArgument


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up services."""
    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        OpenhomeService.INVOKE_PIN,
        entity_domain=MEDIA_PLAYER_DOMAIN,
        schema={probatio.Required(OpenhomeServiceArgument.PIN): cv.positive_int},
        func="async_invoke_pin",
    )
