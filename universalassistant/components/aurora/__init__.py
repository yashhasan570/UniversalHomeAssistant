"""The Aurora integration."""

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from .const import CONF_THRESHOLD, DEFAULT_THRESHOLD
from .coordinator import AuroraConfigEntry, AuroraDataUpdateCoordinator

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]


async def async_setup_entry(hass: UniversalAssistant, entry: AuroraConfigEntry) -> None:
    """Set up Aurora from a config entry."""
    coordinator = AuroraDataUpdateCoordinator(hass=hass, config_entry=entry)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(update_listener))


async def update_listener(hass: UniversalAssistant, entry: AuroraConfigEntry) -> None:
    """Handle options update."""
    entry.runtime_data.threshold = int(
        entry.options.get(CONF_THRESHOLD, DEFAULT_THRESHOLD)
    )
    # refresh the state of the visibility alert binary sensor
    await entry.runtime_data.async_request_refresh()


async def async_unload_entry(hass: UniversalAssistant, entry: AuroraConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
