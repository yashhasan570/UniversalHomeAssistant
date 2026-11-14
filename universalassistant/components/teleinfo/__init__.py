"""The Teleinfo integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import TeleinfoConfigEntry, TeleinfoCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: TeleinfoConfigEntry) -> None:
    """Set up Teleinfo from a config entry."""
    coordinator = TeleinfoCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: TeleinfoConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
