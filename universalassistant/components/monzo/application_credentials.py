"""application_credentials platform the Monzo integration."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import __HAC_KEEP__

OAUTH2_AUTHORIZE = "https://auth.monzo.com"
OAUTH2_TOKEN = "https://api.monzo.com/oauth2/token"


async def async_get_authorization_server(hass: __HAC_KEEP__) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
