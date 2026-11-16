"""Provides diagnostics for the Universal Home Assistant Connect ZBT-2 integration."""

from typing import Any

from universalassistant.core import UniversalAssistant

from . import UniversalAssistantConnectZBT2ConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: UniversalAssistantConnectZBT2ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return {"config_entry": config_entry.as_dict()}
