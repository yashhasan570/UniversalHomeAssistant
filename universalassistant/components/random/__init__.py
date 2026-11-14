"""The random component."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__

from .const import DOMAIN

__all__ = [
    "DOMAIN",
]


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Set up a config entry."""
    await hass.config_entries.async_forward_entry_setups(
        entry, (entry.options["entity_type"],)
    )


async def async_unload_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(
        entry, (entry.options["entity_type"],)
    )
