"""Diagnostics for the EHEIM Digital integration."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from .coordinator import EheimDigitalConfigEntry

TO_REDACT = {"emailAddr", "usrName", "api_usrName", "api_password"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: EheimDigitalConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return async_redact_data(
        {"entry": entry.as_dict(), "data": entry.runtime_data.data}, TO_REDACT
    )
