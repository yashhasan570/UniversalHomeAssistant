"""The Monarch Money integration."""

from typedmonarchmoney import TypedMonarchMoney

from universalassistant.const import CONF_TOKEN, Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import MonarchMoneyConfigEntry, MonarchMoneyDataUpdateCoordinator

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(
    hass: __HAC_KEEP__, entry: MonarchMoneyConfigEntry
) -> None:
    """Set up Monarch Money from a config entry."""
    monarch_client = TypedMonarchMoney(token=entry.data.get(CONF_TOKEN))

    mm_coordinator = MonarchMoneyDataUpdateCoordinator(hass, entry, monarch_client)
    await mm_coordinator.async_config_entry_first_refresh()
    entry.runtime_data = mm_coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, entry: MonarchMoneyConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
