"""Provides diagnostics for the __HA_KEEP__ Connect ZBT-2 integration."""

from typing import Any

from universalassistant.core import __HAC_KEEP__

from . import __HAC_KEEP__ConnectZBT2ConfigEntry


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, config_entry: __HAC_KEEP__ConnectZBT2ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {"config_entry": config_entry.as_dict()}
