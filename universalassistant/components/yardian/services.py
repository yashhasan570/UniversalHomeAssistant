"""Services for the Yardian integration."""

import probatio

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers import config_validation as cv, service
from universalassistant.helpers.typing import VolDictType

from .const import DOMAIN, YardianService, YardianServiceArgument

SERVICE_SCHEMA_START_IRRIGATION: VolDictType = {
    probatio.Required(YardianServiceArgument.DURATION): cv.positive_int,
}


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Set up the services for the Yardian integration."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        YardianService.START_IRRIGATION,
        entity_domain=SWITCH_DOMAIN,
        schema=SERVICE_SCHEMA_START_IRRIGATION,
        func="async_turn_on",
    )
