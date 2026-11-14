"""Config flow for Fjäråskupan integration."""

from fjaraskupan import UUID_SERVICE

from universalassistant.components.bluetooth import async_discovered_service_info
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.config_entry_flow import register_discovery_flow

from .const import DOMAIN


async def _async_has_devices(hass: __HAC_KEEP__) -> bool:
    """Return if there are devices that can be discovered."""

    service_infos = async_discovered_service_info(hass)

    for service_info in service_infos:
        uuids = service_info.service_uuids
        if str(UUID_SERVICE) in uuids:
            return True

    return False


register_discovery_flow(DOMAIN, "Fjäråskupan", _async_has_devices)
