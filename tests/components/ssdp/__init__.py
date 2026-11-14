"""Tests for the SSDP integration."""

from async_upnp_client.ssdp import udn_from_headers
from async_upnp_client.ssdp_listener import SsdpListener
from async_upnp_client.utils import CaseInsensitiveDict

from universalassistant.components import ssdp
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util


async def init_ssdp_component(hass: UniversalAssistant) -> SsdpListener:
    """Initialize ssdp component and get SsdpListener."""
    await async_setup_component(hass, ssdp.DOMAIN, {ssdp.DOMAIN: {}})
    await hass.async_block_till_done()
    return hass.data[ssdp.DOMAIN][ssdp.SSDP_SCANNER]._ssdp_listeners[0]


def _ssdp_headers(headers) -> CaseInsensitiveDict:
    """Create a CaseInsensitiveDict with headers and a timestamp."""
    ssdp_headers = CaseInsensitiveDict(headers, _timestamp=dt_util.naive_now())
    ssdp_headers["_udn"] = udn_from_headers(ssdp_headers)
    return ssdp_headers
