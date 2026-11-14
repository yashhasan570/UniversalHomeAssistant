"""The AirTouch4 integration."""

from airtouch4pyapi import AirTouch

from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryNotReady

from .coordinator import AirTouch4ConfigEntry, AirtouchDataUpdateCoordinator

PLATFORMS = [Platform.CLIMATE]


async def async_setup_entry(hass: UniversalAssistant, entry: AirTouch4ConfigEntry) -> None:
    """Set up AirTouch4 from a config entry."""
    host = entry.data[CONF_HOST]
    airtouch = AirTouch(host)
    await airtouch.UpdateInfo()
    info = airtouch.GetAcs()
    if not info:
        raise ConfigEntryNotReady
    coordinator = AirtouchDataUpdateCoordinator(hass, entry, airtouch)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: AirTouch4ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
