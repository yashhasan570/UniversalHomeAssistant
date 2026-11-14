"""The APsystems local API integration."""

from APsystemsEZ1 import APsystemsEZ1M

from universalassistant.const import CONF_IP_ADDRESS, CONF_PORT, Platform
from universalassistant.core import __HAC_KEEP__

from .const import DEFAULT_PORT
from .coordinator import ApSystemsConfigEntry, ApSystemsData, ApSystemsDataCoordinator

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SENSOR,
    Platform.SWITCH,
]


async def async_setup_entry(hass: __HAC_KEEP__, entry: ApSystemsConfigEntry) -> None:
    """Set up this integration using UI."""
    api = APsystemsEZ1M(
        ip_address=entry.data[CONF_IP_ADDRESS],
        port=entry.data.get(CONF_PORT, DEFAULT_PORT),
        timeout=8,
        enable_debounce=True,
    )
    coordinator = ApSystemsDataCoordinator(hass, entry, api)
    await coordinator.async_config_entry_first_refresh()
    assert entry.unique_id
    entry.runtime_data = ApSystemsData(
        coordinator=coordinator, device_id=entry.unique_id
    )
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)


async def async_unload_entry(hass: __HAC_KEEP__, entry: ApSystemsConfigEntry) -> None:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms_or_raise(entry, PLATFORMS)
