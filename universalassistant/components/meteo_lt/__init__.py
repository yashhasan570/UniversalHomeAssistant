"""The Meteo.lt integration."""

from universalassistant.core import __HAC_KEEP__

from .const import CONF_PLACE_CODE, PLATFORMS
from .coordinator import MeteoLtConfigEntry, MeteoLtUpdateCoordinator


async def async_setup_entry(hass: __HAC_KEEP__, entry: MeteoLtConfigEntry) -> None:
    """Set up Meteo.lt from a config entry."""

    coordinator = MeteoLtUpdateCoordinator(hass, entry.data[CONF_PLACE_CODE], entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: MeteoLtConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
