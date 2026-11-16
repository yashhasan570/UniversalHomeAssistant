"""Marantz IR Remote integration for Universal Home Assistant."""

from dataclasses import dataclass

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

PLATFORMS = [Platform.BUTTON, Platform.MEDIA_PLAYER]


@dataclass
class MarantzIrRuntimeData:
    """Runtime data for a Marantz IR config entry.

    The RC-5 toggle bit must alternate between distinct key presses so
    the receiver can distinguish a new press from a held-down repeat.
    The toggle is tracked at the device level (one value per config
    entry) so all entities of a config entry share it.
    """

    toggle: int = 0


type MarantzIrConfigEntry = ConfigEntry[MarantzIrRuntimeData]


async def async_setup_entry(hass: UniversalAssistant, entry: MarantzIrConfigEntry) -> None:
    """Set up Marantz IR from a config entry."""
    entry.runtime_data = MarantzIrRuntimeData()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: MarantzIrConfigEntry) -> None:
    """Unload a Marantz IR config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
