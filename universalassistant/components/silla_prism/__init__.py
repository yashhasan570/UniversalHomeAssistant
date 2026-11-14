"""The Silla Prism integration."""

from universalassistant.core import __HAC_KEEP__

from .const import PLATFORMS
from .coordinator import PrismConfigEntry, PrismCoordinator


async def async_setup_entry(hass: __HAC_KEEP__, entry: PrismConfigEntry) -> None:
    """Set up Silla Prism from a config entry."""
    coordinator = PrismCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: PrismConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
