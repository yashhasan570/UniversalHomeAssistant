"""The Voice app, as a __HA_KEEP__ app managed by the Supervisor."""

import logging

from universalassistant.components.hassio import AddonManager
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers.singleton import singleton

from .const import DOMAIN

APP_NAME = "Voice"
APP_SLUG = "core_voice"

DATA_APP_MANAGER = f"{DOMAIN}_app_manager"

_LOGGER = logging.getLogger(__name__)


@singleton(DATA_APP_MANAGER)
@callback
def get_app_manager(hass: __HAC_KEEP__) -> AddonManager:
    """Get the app manager."""
    return AddonManager(hass, _LOGGER, APP_NAME, APP_SLUG)
