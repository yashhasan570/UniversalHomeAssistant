"""Refoss helpers functions."""

from refoss_ha.discovery import Discovery

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import singleton


@singleton.singleton("refoss_discovery_server")
async def refoss_discovery_server(hass: UniversalAssistant) -> Discovery:
    """Get refoss Discovery server."""
    discovery_server = Discovery()
    await discovery_server.initialize()
    return discovery_server
