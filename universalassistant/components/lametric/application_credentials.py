"""Application credentials platform for LaMetric."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url="https://developer.lametric.com/api/v2/oauth2/authorize",
        token_url="https://developer.lametric.com/api/v2/oauth2/token",
    )
