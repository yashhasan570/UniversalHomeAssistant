"""Utility helpers for the WiiM integration."""

from urllib.parse import urlparse

from async_upnp_client.utils import async_get_local_ip

from universalassistant.components.network import async_get_source_ip
from universalassistant.core import UniversalAssistant


async def async_get_event_callback_host(hass: UniversalAssistant, upnp_location: str) -> str:
    """Return the address a WiiM device should send UPnP events to."""
    try:
        _, local_ip = await async_get_local_ip(upnp_location, hass.loop)
    except OSError:
        # No route to the device. Fall back to the address Universal Home Assistant
        # announces on, which is what zeroconf and ssdp use.
        if host := urlparse(upnp_location).hostname:
            return await async_get_source_ip(hass, target_ip=host)
        return await async_get_source_ip(hass)

    return local_ip
