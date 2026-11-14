"""Support for Epson projector."""

from enum import StrEnum

from epson_projector.const import CMODE_LIST_SET
import probatio

from universalassistant.components.media_player import DOMAIN as MEDIA_PLAYER_DOMAIN
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers import config_validation as cv, service

from .const import DOMAIN


class EpsonService(StrEnum):
    """Store keys for Epson services."""

    SELECT_CMODE = "select_cmode"


class EpsonServiceArgument(StrEnum):
    """Store keys for Epson service arguments."""

    CMODE = "cmode"


@callback
def async_setup_services(hass: UniversalAssistant) -> None:
    """Set up services."""
    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        EpsonService.SELECT_CMODE,
        entity_domain=MEDIA_PLAYER_DOMAIN,
        schema={
            probatio.Required(EpsonServiceArgument.CMODE): probatio.All(
                cv.string, probatio.Any(*CMODE_LIST_SET)
            )
        },
        func="select_cmode",
    )
