"""The launch_library component."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import LaunchLibraryConfigEntry, LaunchLibraryCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: LaunchLibraryConfigEntry
) -> None:
    """Set up this integration using UI."""

    coordinator = LaunchLibraryCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: LaunchLibraryConfigEntry
) -> None:
    """Handle removal of an entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
