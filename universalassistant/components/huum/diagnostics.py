"""Diagnostics support for Huum."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import HuumConfigEntry

TO_REDACT_DATA = {"sauna_name", "payment_end_date"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: HuumConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data

    return {
        "entry": {
            "version": entry.version,
        },
        "coordinator": {
            "last_update_success": coordinator.last_update_success,
            "last_exception": (
                str(coordinator.last_exception) if coordinator.last_exception else None
            ),
        },
        "data": async_redact_data(coordinator.data.to_dict(), TO_REDACT_DATA),
    }
