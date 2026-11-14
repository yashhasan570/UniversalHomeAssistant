"""application_credentials platform for the august integration."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant

OAUTH2_AUTHORIZE = "https://auth.august.com/authorization"
OAUTH2_TOKEN = "https://auth.august.com/access_token"


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
