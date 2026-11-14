"""The worldclock component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__

from .const import PLATFORMS


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up Worldclock from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload World clock config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
