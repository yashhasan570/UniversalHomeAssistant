"""Diagnostics platform for Tailwind."""

from typing import Any

from universalassistant.core import UniversalAssistant

from .coordinator import TailwindConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: TailwindConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.data.to_dict()
