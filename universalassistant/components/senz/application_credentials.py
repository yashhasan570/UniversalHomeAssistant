"""Application credentials platform for senz."""

from pysenz import AUTHORIZATION_ENDPOINT, TOKEN_ENDPOINT

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import __HAC_KEEP__


async def async_get_authorization_server(hass: __HAC_KEEP__) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=AUTHORIZATION_ENDPOINT,
        token_url=TOKEN_ENDPOINT,
    )
