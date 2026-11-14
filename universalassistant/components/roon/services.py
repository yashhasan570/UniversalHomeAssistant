"""MediaPlayer platform for Roon integration."""

from enum import StrEnum

import probatio

from universalassistant.components.media_player import DOMAIN as MEDIA_PLAYER_DOMAIN
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers import config_validation as cv, service

from .const import DOMAIN


class RoonService(StrEnum):
    """Store keys for Roon services."""

    TRANSFER = "transfer"


class RoonServiceArgument(StrEnum):
    """Store keys for Roon service arguments."""

    TRANSFER_ID = "transfer_id"


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up services."""
    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        RoonService.TRANSFER,
        entity_domain=MEDIA_PLAYER_DOMAIN,
        schema={probatio.Required(RoonServiceArgument.TRANSFER_ID): cv.entity_id},
        func="async_transfer",
    )
