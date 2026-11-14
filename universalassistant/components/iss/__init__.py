"""The iss component."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import IssConfigEntry, IssDataUpdateCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: IssConfigEntry) -> None:
    """Set up this integration using UI."""
    coordinator = IssDataUpdateCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    entry.async_on_unload(entry.add_update_listener(update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: IssConfigEntry) -> None:
    """Handle removal of an entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


async def update_listener(hass: __HAC_KEEP__, entry: IssConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)
