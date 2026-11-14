"""Provides diagnostics for Tado."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import TadoConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: TadoConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a Tado config entry."""

    rate_limit = config_entry.runtime_data.get_rate_limit()
    return {"data": config_entry.runtime_data.data, "rate_limit": rate_limit}
