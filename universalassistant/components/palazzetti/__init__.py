"""The Palazzetti integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import PalazzettiConfigEntry, PalazzettiDataUpdateCoordinator

PLATFORMS: list[Platform] = [
    Platform.BUTTON,
    Platform.CLIMATE,
    Platform.NUMBER,
    Platform.SENSOR,
]


async def async_setup_entry(hass: __HAC_KEEP__, entry: PalazzettiConfigEntry) -> None:
    """Set up Palazzetti from a config entry."""

    coordinator = PalazzettiDataUpdateCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: PalazzettiConfigEntry) -> None:
    """Unload a config entry."""

    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
