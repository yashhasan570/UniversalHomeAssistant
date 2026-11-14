"""The qnap component."""

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__

from .coordinator import QnapConfigEntry, QnapCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


async def async_setup_entry(hass: __HAC_KEEP__, config_entry: QnapConfigEntry) -> None:
    """Set the config entry up."""
    coordinator = QnapCoordinator(hass, config_entry)
    await coordinator.async_config_entry_first_refresh()
    config_entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(config_entry, PLATFORMS)


async def async_unload_entry(
    hass: __HAC_KEEP__, config_entry: QnapConfigEntry
) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(config_entry, PLATFORMS)
