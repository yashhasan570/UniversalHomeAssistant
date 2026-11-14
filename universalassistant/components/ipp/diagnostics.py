"""Diagnostics support for Internet Printing Protocol (IPP)."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import IPPConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: IPPConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = config_entry.runtime_data

    return {
        "entry": {
            "data": {
                **config_entry.data,
            },
            "unique_id": config_entry.unique_id,
        },
        "data": coordinator.data.as_dict(),
    }
