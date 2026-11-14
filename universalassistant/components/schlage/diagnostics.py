"""Diagnostics support for Schlage."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from .coordinator import SchlageConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__,
    config_entry: SchlageConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = config_entry.runtime_data
    # NOTE: Schlage diagnostics are already redacted.
    return {"locks": [ld.lock.get_diagnostics() for ld in coordinator.data.values()]}
