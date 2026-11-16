"""The Raspberry Pi integration."""

from universalassistant.components.hassio import HassioNotReadyError, get_os_info
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryError, ConfigEntryNotReady
from universalassistant.helpers.hassio import is_hassio

from .const import DOMAIN

PLATFORMS = [Platform.UPDATE]


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Set up a Raspberry Pi config entry."""
    if not is_hassio(hass):
        # Not running under supervisor, Universal Home Assistant may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="not_hassio",
        )

    try:
        os_info = get_os_info(hass)
    except HassioNotReadyError as err:
        raise ConfigEntryNotReady from err

    board: str | None
    if (board := os_info.get("board")) is None or not board.startswith("rpi"):
        # Not running on a Raspberry Pi, Universal Home Assistant may have been migrated
        hass.async_create_task(hass.config_entries.async_remove(entry.entry_id))
        raise ConfigEntryError(
            translation_domain=DOMAIN,
            translation_key="unsupported_board",
            translation_placeholders={"board": str(board)},
        )

    await hass.config_entries.flow.async_init(
        "rpi_power", context={"source": "onboarding"}
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
