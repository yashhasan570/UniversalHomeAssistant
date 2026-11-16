"""application_credentials platform the yale integration."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant

OAUTH2_AUTHORIZE = "https://oauth.aaecosystem.com/authorize"
OAUTH2_TOKEN = "https://oauth.aaecosystem.com/access_token"


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
