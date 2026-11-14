"""Diagnostics support for ONVIF."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__

from .device import ONVIFConfigEntry

REDACT_CONFIG = {CONF_HOST, CONF_PASSWORD, CONF_USERNAME}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: ONVIFConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    device = entry.runtime_data
    data: dict[str, Any] = {}

    data["config"] = async_redact_data(entry.as_dict(), REDACT_CONFIG)
    data["device"] = {
        "info": asdict(device.info),
        "capabilities": asdict(device.capabilities),
        "profiles": [asdict(profile) for profile in device.profiles],
        "services": {
            str(key): service.url for key, service in device.device.services.items()
        },
        "xaddrs": device.device.xaddrs,
    }
    data["events"] = {
        "webhook_manager_state": device.events.webhook_manager.state,
        "pullpoint_manager_state": device.events.pullpoint_manager.state,
    }

    return data
