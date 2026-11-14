"""Initialize the Redgtech integration for __HA_KEEP__."""

import logging

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import RedgtechConfigEntry, RedgtechDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


PLATFORMS = [Platform.SWITCH]


async def async_setup_entry(hass: __HAC_KEEP__, entry: RedgtechConfigEntry) -> None:
    """Set up Redgtech from a config entry."""
    _LOGGER.debug("Setting up Redgtech entry: %s", entry.entry_id)
    coordinator = RedgtechDataUpdateCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    _LOGGER.debug("Successfully set up Redgtech entry: %s", entry.entry_id)


async def async_unload_entry(hass: __HAC_KEEP__, entry: RedgtechConfigEntry) -> None:
    """Unload a config entry."""
    _LOGGER.debug("Unloading Redgtech entry: %s", entry.entry_id)
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
