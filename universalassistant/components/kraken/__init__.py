"""The kraken integration."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.dispatcher import async_dispatcher_send

from .const import DISPATCH_CONFIG_UPDATED
from .coordinator import KrakenConfigEntry, KrakenData

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: __HAC_KEEP__, entry: KrakenConfigEntry) -> None:
    """Set up kraken from a config entry."""
    kraken_data = KrakenData(hass, entry)
    await kraken_data.async_setup()
    entry.runtime_data = kraken_data
    entry.async_on_unload(entry.add_update_listener(async_options_updated))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, config_entry: KrakenConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(config_entry, PLATFORMS)


async def async_options_updated(
    hass: __HAC_KEEP__, config_entry: KrakenConfigEntry
) -> None:
    """Triggered by config entry options updates."""
    async_dispatcher_send(hass, DISPATCH_CONFIG_UPDATED, hass, config_entry)
