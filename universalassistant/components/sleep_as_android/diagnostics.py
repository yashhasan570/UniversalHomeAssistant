"""Diagnostics platform for Sleep as Android integration."""

from typing import Any

from universalassistant.core import UniversalAssistant

from . import SleepAsAndroidConfigEntry


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, config_entry: SleepAsAndroidConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""

    return {
        "config_entry_data": {"cloudhook": config_entry.data["cloudhook"]},
    }
