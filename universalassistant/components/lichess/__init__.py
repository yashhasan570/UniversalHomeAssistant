"""The Lichess integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import LichessConfigEntry, LichessCoordinator

_PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: UniversalAssistant, entry: LichessConfigEntry) -> None:
    """Set up Lichess from a config entry."""

    coordinator = LichessCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: LichessConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, _PLATFORMS)
