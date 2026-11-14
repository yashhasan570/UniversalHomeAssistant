"""Refoss helpers functions."""

from refoss_ha.discovery import Discovery

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import singleton


@singleton.singleton("refoss_discovery_server")
async def refoss_discovery_server(hass: __HAC_KEEP__) -> Discovery:
    """Get refoss Discovery server."""
    discovery_server = Discovery()
    await discovery_server.initialize()
    return discovery_server
