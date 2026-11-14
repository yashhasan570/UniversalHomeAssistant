"""Support for Powerfox Local diagnostics."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import PowerfoxLocalConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: PowerfoxLocalConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for Powerfox Local config entry."""
    coordinator = entry.runtime_data

    return {
        "power": coordinator.data.power,
        "energy_usage": coordinator.data.energy_usage,
        "energy_usage_high_tariff": coordinator.data.energy_usage_high_tariff,
        "energy_usage_low_tariff": coordinator.data.energy_usage_low_tariff,
        "energy_return": coordinator.data.energy_return,
    }
