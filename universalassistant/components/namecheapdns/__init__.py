"""Support for namecheap DNS services."""

import logging

from universalassistant.core import UniversalAssistant, async_noop

from .coordinator import NamecheapConfigEntry, NamecheapDnsUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: UniversalAssistant, entry: NamecheapConfigEntry) -> None:
    """Set up Namecheap DynamicDNS from a config entry."""

    coordinator = NamecheapDnsUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator

    # Add a dummy listener as we do not have regular entities
    entry.async_on_unload(coordinator.async_add_listener(async_noop))


async def async_unload_entry(hass: UniversalAssistant, entry: NamecheapConfigEntry) -> None:
    """Unload a config entry."""
