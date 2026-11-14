"""Application credentials platform for spotify."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url="https://accounts.spotify.com/authorize",
        token_url="https://accounts.spotify.com/api/token",
    )
