"""Provide add-on management."""

from universalassistant.components.hassio import AddonManager
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers.singleton import singleton

from .const import ADDON_SLUG, DOMAIN, LOGGER

DATA_ADDON_MANAGER = f"{DOMAIN}_addon_manager"


@singleton(DATA_ADDON_MANAGER)
@callback
def get_addon_manager(hass: UniversalAssistant) -> AddonManager:
    """Get the add-on manager."""
    return AddonManager(hass, LOGGER, "Matter Server", ADDON_SLUG)
