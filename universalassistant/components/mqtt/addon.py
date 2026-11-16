"""Provide MQTT add-on management.

Currently only supports the official mosquitto add-on.
"""

from universalassistant.components.hassio import AddonManager
from universalassistant.core import UniversalAssistant, callback
from universalassistant.helpers.singleton import singleton

from .const import DOMAIN, LOGGER

ADDON_SLUG = "core_mosquitto"
DATA_ADDON_MANAGER = f"{DOMAIN}_addon_manager"


@singleton(DATA_ADDON_MANAGER)
@callback
def get_addon_manager(hass: UniversalAssistant) -> AddonManager:
    """Get the add-on manager."""
    return AddonManager(hass, LOGGER, "Mosquitto Mqtt Broker", ADDON_SLUG)
