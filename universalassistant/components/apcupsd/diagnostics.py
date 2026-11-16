"""Diagnostics support for APCUPSD."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import APCUPSdConfigEntry

TO_REDACT = {"SERIALNO", "HOSTNAME"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: APCUPSdConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    data = coordinator.data
    return async_redact_data(data, TO_REDACT)
