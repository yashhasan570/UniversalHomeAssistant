"""Component for the Slide local API."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import SlideConfigEntry, SlideCoordinator

PLATFORMS = [Platform.BUTTON, Platform.COVER, Platform.SWITCH]


async def async_setup_entry(hass: UniversalAssistant, entry: SlideConfigEntry) -> None:
    """Set up the slide_local integration."""

    coordinator = SlideCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: SlideConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
