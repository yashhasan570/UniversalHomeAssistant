"""Services for the Logitech Harmony Hub integration."""

from enum import StrEnum

import probatio

from universalassistant.components.remote import DOMAIN as REMOTE_DOMAIN
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers import config_validation as cv, service
from universalassistant.helpers.typing import VolDictType

from .const import DOMAIN


class HarmonyService(StrEnum):
    """Store keys for Logitech Harmony Hub services."""

    SYNC = "sync"
    CHANGE_CHANNEL = "change_channel"


class HarmonyServiceArgument(StrEnum):
    """Store keys for Logitech Harmony Hub service arguments."""

    CHANNEL = "channel"


HARMONY_CHANGE_CHANNEL_SCHEMA: VolDictType = {
    probatio.Required(HarmonyServiceArgument.CHANNEL): cv.positive_int,
}


@callback
def async_setup_services(hass: __HAC_KEEP__) -> None:
    """Set up the services for the Logitech Harmony Hub integration."""

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        HarmonyService.SYNC,
        entity_domain=REMOTE_DOMAIN,
        schema=None,
        func="sync",
    )

    service.async_register_platform_entity_service(
        hass,
        DOMAIN,
        HarmonyService.CHANGE_CHANNEL,
        entity_domain=REMOTE_DOMAIN,
        schema=HARMONY_CHANGE_CHANNEL_SCHEMA,
        func="change_channel",
    )
