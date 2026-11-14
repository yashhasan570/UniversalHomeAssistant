"""Provides diagnostics for EcoWitt."""

from typing import Any

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.device_registry import AnyDeviceEntry

from . import EcowittConfigEntry
from .const import DOMAIN


async def async_get_device_diagnostics(
    hass: __HAC_KEEP__, entry: EcowittConfigEntry, device: AnyDeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device entry."""
    ecowitt = entry.runtime_data
    station_id = next(item[1] for item in device.identifiers if item[0] == DOMAIN)

    station = ecowitt.stations[station_id]

    return {
        "device": {
            "name": station.station,
            "model": station.model,
            "frequency": station.frequence,  # codespell:ignore frequence
            "version": station.version,
        },
        "raw": ecowitt.last_values[station_id],
        "sensors": {
            sensor.key: sensor.value
            for sensor in ecowitt.sensors.values()
            if sensor.station.key == station_id
        },
    }
