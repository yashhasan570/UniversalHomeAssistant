"""application_credentials platform the Ekey Bionyx integration."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant

from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
