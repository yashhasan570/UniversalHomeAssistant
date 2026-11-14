"""Application credentials platform for yolink."""

from yolink.const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import __HAC_KEEP__


async def async_get_authorization_server(hass: __HAC_KEEP__) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
