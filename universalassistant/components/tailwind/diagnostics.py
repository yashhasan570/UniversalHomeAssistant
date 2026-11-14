"""Diagnostics platform for Tailwind."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import TailwindConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: TailwindConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return entry.runtime_data.data.to_dict()
