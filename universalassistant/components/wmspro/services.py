"""Services for WMS WebControl pro."""

import probatio

from universalassistant.components.cover import DOMAIN as COVER_DOMAIN, CoverEntityFeature
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers import service

from .const import DOMAIN, WebControlProService, WebControlProServiceArgument


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up services for WMS WebControl pro."""
    service.async_register_platform_entity_service(
        hass,
        service_domain=DOMAIN,
        service_name=WebControlProService.SET_COVER_POSITION_AND_TILT,
        entity_domain=COVER_DOMAIN,
        func="async_set_cover_position_and_tilt",
        required_features=[
            CoverEntityFeature.SET_POSITION | CoverEntityFeature.SET_TILT_POSITION
        ],
        schema={
            probatio.Required(WebControlProServiceArgument.POSITION): probatio.All(
                probatio.Coerce(int), probatio.Percentage()
            ),
            probatio.Required(WebControlProServiceArgument.TILT_POSITION): probatio.All(
                probatio.Coerce(int), probatio.Percentage()
            ),
        },
    )
