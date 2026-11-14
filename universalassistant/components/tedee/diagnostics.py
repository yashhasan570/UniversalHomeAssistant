"""Diagnostics support for tedee."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import TedeeConfigEntry

TO_REDACT = {
    "id",
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: TedeeConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    # dict has sensitive info as key, redact manually
    data = {
        index: lock.to_dict()
        for index, (_, lock) in enumerate(coordinator.tedee_client.locks_dict.items())
    }
    return async_redact_data(data, TO_REDACT)
