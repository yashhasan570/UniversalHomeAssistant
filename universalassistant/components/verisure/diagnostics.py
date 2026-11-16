"""Diagnostics support for Verisure."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import VerisureConfigEntry

TO_REDACT = {
    "date",
    "area",
    "deviceArea",
    "name",
    "time",
    "reportTime",
    "userString",
}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: VerisureConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(entry.runtime_data.data, TO_REDACT)
