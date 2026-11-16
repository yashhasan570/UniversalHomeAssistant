"""Diagnostics for SteamVR Base Station."""

from dataclasses import asdict
from typing import Any

from universalassistant.components.bluetooth import async_last_service_info
from universalassistant.components.diagnostics import async_redact_data
from universalassistant.core import UniversalAssistant

from .coordinator import SteamVRBaseStationConfigEntry

TO_REDACT = {"discovery_keys", "serial", "title", "unique_id"}


async def async_get_config_entry_diagnostics(
    hass: UniversalAssistant, entry: SteamVRBaseStationConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    last_advertisement = None
    if service_info := async_last_service_info(
        hass, coordinator.address, connectable=True
    ):
        last_advertisement = {
            "rssi": service_info.rssi,
            "manufacturer_data": {
                company_id: data.hex()
                for company_id, data in service_info.manufacturer_data.items()
            },
        }
    return {
        "entry": async_redact_data(entry.as_dict(), TO_REDACT),
        "device_info": async_redact_data(asdict(coordinator.device_info), TO_REDACT),
        "available": coordinator.available,
        "state": asdict(coordinator.station.state),
        "supports_standby": coordinator.station.supports_standby,
        "last_advertisement": last_advertisement,
    }
