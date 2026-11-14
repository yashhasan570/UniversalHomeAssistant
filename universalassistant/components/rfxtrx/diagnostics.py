"""Diagnostics support for RFXCOM RFXtrx."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from . import RfxtrxConfigEntry

TO_REDACT = {"host"}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: RfxtrxConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
    }
