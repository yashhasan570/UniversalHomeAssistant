"""Services for the Hayward Omnilogic integration."""

from enum import StrEnum

import probatio

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers import config_validation as cv, service

from .const import DOMAIN


class OmniLogicService(StrEnum):
    """Store keys for Hayward Omnilogic services."""

    SET_PUMP_SPEED = "set_pump_speed"


class OmniLogicServiceArgument(StrEnum):
    """Store keys for Hayward Omnilogic service arguments."""

    SPEED = "speed"


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up the services for the Hayward Omnilogic integration."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        OmniLogicService.SET_PUMP_SPEED,
        entity_domain=SWITCH_DOMAIN,
        schema={probatio.Required(OmniLogicServiceArgument.SPEED): cv.positive_int},
        func="async_set_speed",
    )
