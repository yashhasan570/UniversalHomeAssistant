"""Application credentials platform for the Miele integration."""

from pymiele import OAUTH2_AUTHORIZE, OAUTH2_TOKEN

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import __HAC_KEEP__


async def async_get_authorization_server(hass: __HAC_KEEP__) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )


async def async_get_description_placeholders(hass: __HAC_KEEP__) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "register_url": "https://www.miele.com/f/com/en/register_api.aspx",
    }
