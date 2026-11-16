"""The ista Ecotrend integration."""

import logging

from pyecotrend_ista import PyEcotrendIsta

from universalassistant.components.recorder import get_instance
from universalassistant.const import CONF_EMAIL, CONF_PASSWORD, Platform
from universalassistant.core import UniversalAssistant

from .const import DOMAIN
from .coordinator import IstaConfigEntry, IstaCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: IstaConfigEntry) -> None:
    """Set up ista EcoTrend from a config entry."""
    ista = PyEcotrendIsta(
        entry.data[CONF_EMAIL],
        entry.data[CONF_PASSWORD],
    )

    coordinator = IstaCoordinator(hass, entry, ista)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: IstaConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)


async def async_remove_entry(hass: UniversalAssistant, entry: IstaConfigEntry) -> None:
    """Handle removal of an entry."""
    statistic_ids = [f"{DOMAIN}:{name}" for name in entry.options.values()]
    get_instance(hass).async_clear_statistics(statistic_ids)
