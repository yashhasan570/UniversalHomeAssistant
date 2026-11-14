"""The Helty Flow integration."""

from pyhelty import HeltyClient

from universalassistant.const import CONF_HOST, Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import HeltyConfigEntry, HeltyDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.BUTTON, Platform.FAN, Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: HeltyConfigEntry) -> None:
    """Set up Helty Flow from a config entry."""
    client = HeltyClient(entry.data[CONF_HOST])
    coordinator = HeltyDataUpdateCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: HeltyConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
