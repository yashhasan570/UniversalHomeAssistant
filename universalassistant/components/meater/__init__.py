"""The Meater Temperature Probe integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .const import MEATER_DATA
from .coordinator import MeaterConfigEntry, MeaterCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: MeaterConfigEntry) -> None:
    """Set up Meater Temperature Probe from a config entry."""

    coordinator = MeaterCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(MEATER_DATA, set())

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: UniversalAssistant, entry: MeaterConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
    hass.data[MEATER_DATA] = hass.data[MEATER_DATA] - entry.runtime_data.found_probes
