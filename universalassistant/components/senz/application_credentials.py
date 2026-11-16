"""Application credentials platform for senz."""

from pysenz import AUTHORIZATION_ENDPOINT, TOKEN_ENDPOINT

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=AUTHORIZATION_ENDPOINT,
        token_url=TOKEN_ENDPOINT,
    )
