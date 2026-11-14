"""Config flow for Gree."""

from greeclimate.discovery import Discovery

from universalassistant.components.network import async_get_ipv4_broadcast_addresses
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_entry_flow

from .const import DISCOVERY_TIMEOUT, DOMAIN


async def _async_has_devices(hass: __HAC_KEEP__) -> bool:
    """Return if there are devices that can be discovered."""
    gree_discovery = Discovery(DISCOVERY_TIMEOUT)
    bcast_addr = list(await async_get_ipv4_broadcast_addresses(hass))
    devices = await gree_discovery.scan(
        wait_for=DISCOVERY_TIMEOUT, bcast_ifaces=bcast_addr
    )
    return len(devices) > 0


config_entry_flow.register_discovery_flow(DOMAIN, "Gree Climate", _async_has_devices)
