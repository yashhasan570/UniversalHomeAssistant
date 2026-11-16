"""application_credentials platform for YouTube."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        "https://accounts.google.com/o/oauth2/v2/auth",
        "https://oauth2.googleapis.com/token",
    )
