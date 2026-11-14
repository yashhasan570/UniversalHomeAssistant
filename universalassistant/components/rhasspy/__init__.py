"""The Rhasspy integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up Rhasspy from a config entry."""


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
