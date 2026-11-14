"""The Ekey Bionyx integration."""

from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

PLATFORMS: list[Platform] = [Platform.EVENT]


type EkeyBionyxConfigEntry = ConfigEntry


async def async_setup_entry(hass: __HAC_KEEP__, entry: EkeyBionyxConfigEntry) -> None:
    """Set up the Ekey Bionyx config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: EkeyBionyxConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
