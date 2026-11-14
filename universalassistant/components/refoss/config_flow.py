"""Config Flow for Refoss integration."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_entry_flow

from .const import DISCOVERY_TIMEOUT, DOMAIN, LOGGER
from .util import refoss_discovery_server


async def _async_has_devices(hass: UniversalAssistant) -> bool:
    """Return if there are devices that can be discovered."""

    refoss_discovery = await refoss_discovery_server(hass)
    devices = await refoss_discovery.broadcast_msg(wait_for=DISCOVERY_TIMEOUT)
    LOGGER.debug(
        "Discovered devices: [%s]", ", ".join([info.dev_name for info in devices])
    )
    return len(devices) > 0


config_entry_flow.register_discovery_flow(DOMAIN, "Refoss", _async_has_devices)
