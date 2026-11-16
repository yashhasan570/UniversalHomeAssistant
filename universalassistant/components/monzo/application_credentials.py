"""application_credentials platform the Monzo integration."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant

OAUTH2_AUTHORIZE = "https://auth.monzo.com"
OAUTH2_TOKEN = "https://api.monzo.com/oauth2/token"


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
