"""Support to control a Salda Smarty XP/XV ventilation unit."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import SmartyConfigEntry, SmartyCoordinator

PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.FAN,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: UniversalAssistant, entry: SmartyConfigEntry) -> None:
    """Set up the Smarty environment from a config entry."""

    coordinator = SmartyCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: SmartyConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
