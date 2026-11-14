"""Diagnostics support for Sensibo."""

from typing import Any

from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import __HAC_KEEP__

from . import SensiboConfigEntry

TO_REDACT = {
    "location",
    "ssid",
    "id",
    "mac",
    "macAddress",
    "parentDeviceUid",
    "qrId",
    "serial",
    "uid",
    "email",
    "firstName",
    "lastName",
    "username",
    "podUid",
    "deviceUid",
}


async def async_get_config_entry_diagnostics(
    hass: __HAC_KEEP__, entry: SensiboConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for Sensibo config entry."""
    coordinator = entry.runtime_data
    diag_data = {}
    diag_data["raw"] = async_redact_data(coordinator.data.raw, TO_REDACT)
    for device, device_data in coordinator.data.parsed.items():
        diag_data[device] = async_redact_data(device_data.__dict__, TO_REDACT)
    return diag_data
