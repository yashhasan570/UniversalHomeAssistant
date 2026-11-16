"""application_credentials platform the myUplink integration."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant

from .const import DOMAIN, OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )


async def async_get_description_placeholders(hass: UniversalAssistant) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "more_info_url": f"https://www.universalassistant.io/integrations/{DOMAIN}/",
        "create_creds_url": "https://dev.myuplink.com/apps",
        "callback_url": "https://my.universalassistant.io/redirect/oauth",
    }
