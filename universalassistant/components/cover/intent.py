"""Intents for the cover integration."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import intent

from . import INTENT_CLOSE_COVER, INTENT_OPEN_COVER, CoverDeviceClass
from .const import DOMAIN, CoverService


async def async_setup_intents(hass: __HAC_KEEP__) -> None:
    """Set up the cover intents."""
    intent.async_register(
        hass,
        intent.ServiceIntentHandler(
            INTENT_OPEN_COVER,
            DOMAIN,
            CoverService.OPEN,
            description="Opens a cover",
            platforms={DOMAIN},
            required_domains={DOMAIN},
            device_classes={CoverDeviceClass},
        ),
    )
    intent.async_register(
        hass,
        intent.ServiceIntentHandler(
            INTENT_CLOSE_COVER,
            DOMAIN,
            CoverService.CLOSE,
            description="Closes a cover",
            platforms={DOMAIN},
            required_domains={DOMAIN},
            device_classes={CoverDeviceClass},
        ),
    )
