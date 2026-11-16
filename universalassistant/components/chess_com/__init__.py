"""The Chess.com integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .coordinator import ChessConfigEntry, ChessCoordinator

_PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: UniversalAssistant, entry: ChessConfigEntry) -> None:
    """Set up Chess.com from a config entry."""

    coordinator = ChessCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: ChessConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, _PLATFORMS)
