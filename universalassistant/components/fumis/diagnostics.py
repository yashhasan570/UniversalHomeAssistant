"""Diagnostics support for Fumis."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import FumisConfigEntry

TO_REDACT_UNIT = {"id", "ip"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: FumisConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    data = await entry.runtime_data.client.raw_status()
    data["unit"] = async_redact_data(data["unit"], TO_REDACT_UNIT)
    return data
