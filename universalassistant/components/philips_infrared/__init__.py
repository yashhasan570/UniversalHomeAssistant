"""Philips IR Remote integration for __HA_KEEP__."""

from dataclasses import dataclass

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

PLATFORMS = [Platform.MEDIA_PLAYER]


@dataclass
class PhilipsIrRuntimeData:
    """Runtime data for a Philips IR config entry.

    The RC-6 toggle bit must alternate between distinct key presses, or the
    TV reads a second press of the same key as a held-down repeat and
    ignores it. It is tracked per config entry, not per entity, so it keeps
    alternating across every entity that sends commands to the same TV.
    """

    toggle: int = 0


type PhilipsIrConfigEntry = ConfigEntry[PhilipsIrRuntimeData]


async def async_setup_entry(hass: __HAC_KEEP__, entry: PhilipsIrConfigEntry) -> None:
    """Set up Philips IR from a config entry."""
    entry.runtime_data = PhilipsIrRuntimeData()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: PhilipsIrConfigEntry) -> None:
    """Unload a Philips IR config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
