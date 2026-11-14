"""Intents for the lawn mower integration."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import intent

from . import LawnMowerEntityFeature
from .const import DOMAIN, LawnMowerService

INTENT_LANW_MOWER_START_MOWING = "HassLawnMowerStartMowing"
INTENT_LANW_MOWER_DOCK = "HassLawnMowerDock"


async def async_setup_intents(hass: __HAC_KEEP__) -> None:
    """Set up the lawn mower intents."""
    intent.async_register(
        hass,
        intent.ServiceIntentHandler(
            INTENT_LANW_MOWER_START_MOWING,
            DOMAIN,
            LawnMowerService.START_MOWING,
            description="Starts a lawn mower",
            required_domains={DOMAIN},
            platforms={DOMAIN},
            required_features=LawnMowerEntityFeature.START_MOWING,
        ),
    )
    intent.async_register(
        hass,
        intent.ServiceIntentHandler(
            INTENT_LANW_MOWER_DOCK,
            DOMAIN,
            LawnMowerService.DOCK,
            description="Sends a lawn mower to dock",
            required_domains={DOMAIN},
            platforms={DOMAIN},
            required_features=LawnMowerEntityFeature.DOCK,
        ),
    )
