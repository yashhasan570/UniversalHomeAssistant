"""The Xiaomi Weather integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv

from .const import DOMAIN
from .coordinator import XiaomiWeatherConfigEntry, XiaomiWeatherCoordinator

PLATFORMS = [Platform.WEATHER]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: XiaomiWeatherConfigEntry
) -> None:
    """Fetch initial data before setting up platforms."""
    coordinator = XiaomiWeatherCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: XiaomiWeatherConfigEntry
) -> None:
    """Unload entities and their coordinator subscriptions."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
