"""The time_date component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__

from .const import PLATFORMS


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up Time & Date from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload Time & Date config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
