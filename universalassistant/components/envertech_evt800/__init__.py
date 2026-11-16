"""Envertech EVT800 integration."""

from pyenvertechevt800 import EnvertechEVT800

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_IP_ADDRESS, CONF_PORT
from universalassistant.core import UniversalAssistant

from .const import PLATFORMS
from .coordinator import EnvertechEVT800Coordinator

type EnvertechEVT800ConfigEntry = ConfigEntry[EnvertechEVT800Coordinator]


async def async_setup_entry(
    hass: UniversalAssistant, entry: EnvertechEVT800ConfigEntry
) -> None:
    """Set up Envertech EVT800 from a config entry."""
    evt800 = EnvertechEVT800(entry.data[CONF_IP_ADDRESS], entry.data[CONF_PORT])
    evt800.start()

    coordinator = EnvertechEVT800Coordinator(hass, evt800, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: UniversalAssistant, entry: EnvertechEVT800ConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
