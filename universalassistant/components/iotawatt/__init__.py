"""The iotawatt integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import IotawattConfigEntry, IotawattUpdater

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: IotawattConfigEntry) -> None:
    """Set up iotawatt from a config entry."""
    coordinator = IotawattUpdater(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: IotawattConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
