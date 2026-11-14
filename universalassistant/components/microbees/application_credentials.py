"""application_credentials platform the microBees integration."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import __HAC_KEEP__

from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_authorization_server(hass: __HAC_KEEP__) -> AuthorizationServer:
    """Return auth implementation."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )
