"""Provide Universal Universal Home Assistant app management."""

from urllib.parse import urlsplit

from universalassistant.components.hassio import (
    AddonManager,
    HassioNotReadyError,
    get_addons_info,
)
from universalassistant.core import UniversalAssistant, callback
from universalassistant.exceptions import ConfigEntryNotReady
from universalassistant.helpers.hassio import is_hassio
from universalassistant.helpers.singleton import singleton

from .const import APP_NAME, APP_SLUG, DOMAIN, LOGGER

DATA_APP_MANAGER = f"{DOMAIN}_app_manager"


@callback
def async_check_app_running(hass: UniversalAssistant, url: str) -> None:
    """Explain connection failures when the configured local app is offline."""
    if not is_hassio(hass):
        return

    try:
        apps = get_addons_info(hass)
    except HassioNotReadyError:
        return

    hostname = urlsplit(url).hostname
    for info in apps.values():
        if (
            info is not None
            and info["hostname"] == hostname
            and info["state"] in ("stopped", "error", "startup")
        ):
            raise ConfigEntryNotReady(
                translation_domain=DOMAIN,
                translation_key="app_not_running",
                translation_placeholders={"app": info["name"]},
            )


@singleton(DATA_APP_MANAGER)
@callback
def get_app_manager(hass: UniversalAssistant) -> AddonManager:
    """Get the app manager."""
    return AddonManager(hass, LOGGER, APP_NAME, APP_SLUG)
