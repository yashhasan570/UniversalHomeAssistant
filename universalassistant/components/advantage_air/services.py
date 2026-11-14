"""Services for Advantage Air integration."""

import probatio

from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers import config_validation as cv, service

from .const import DOMAIN, AdvantageAirService, AdvantageAirServiceArgument


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Universal Universal Home Assistant services."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        AdvantageAirService.SET_TIME_TO,
        entity_domain=SENSOR_DOMAIN,
        schema={
            probatio.Required(AdvantageAirServiceArgument.MINUTES): cv.positive_int
        },
        func="set_time_to",
    )
