"""Services for the Pi-hole integration."""

from enum import StrEnum

import probatio

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers import config_validation as cv, service

from .const import DOMAIN


class PiHoleService(StrEnum):
    """Store keys for Pi-hole services."""

    DISABLE = "disable"


class PiHoleServiceArgument(StrEnum):
    """Store keys for Pi-hole service arguments."""

    DURATION = "duration"


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up the services for the Pi-hole integration."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        PiHoleService.DISABLE,
        entity_domain=SWITCH_DOMAIN,
        schema={
            probatio.Required(PiHoleServiceArgument.DURATION): probatio.All(
                cv.time_period_str, cv.positive_timedelta
            )
        },
        func="async_disable",
    )
