"""Diagnostics support for Whois."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import WhoisConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: WhoisConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    if (data := entry.runtime_data.data) is None:
        return {}
    return {
        "creation_date": data.creation_date,
        "expiration_date": data.expiration_date,
        "last_updated": data.updated_date,
        "status": data.status,
        "statuses": data.statuses,
        "dnssec": data.dnssec,
    }
