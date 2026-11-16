"""application_credentials platform the Google Photos integration."""

from universalassistant.components.application_credentials import AuthorizationServer
from universalassistant.core import UniversalAssistant

from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )


async def async_get_description_placeholders(hass: UniversalAssistant) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "oauth_consent_url": "https://console.cloud.google.com/apis/credentials/consent",
        "more_info_url": "https://www.universalassistant.io/integrations/google_photos/",
        "oauth_creds_url": "https://console.cloud.google.com/apis/credentials",
    }
