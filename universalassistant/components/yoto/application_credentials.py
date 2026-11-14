"""Application credentials platform for the Yoto integration."""

from universalassistant.components.application_credentials import ClientCredential
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.config_entry_oauth2_flow import (
    LocalOAuth2ImplementationWithPkce,
)

AUTHORIZE_URL = "https://login.yotoplay.com/authorize"
TOKEN_URL = "https://login.yotoplay.com/oauth/token"


async def async_get_auth_implementation(
    hass: UniversalAssistant,
    auth_domain: str,
    credential: ClientCredential,
) -> LocalOAuth2ImplementationWithPkce:
    """Return a Yoto OAuth2 implementation with PKCE."""
    return LocalOAuth2ImplementationWithPkce(
        hass,
        auth_domain,
        credential.client_id,
        AUTHORIZE_URL,
        TOKEN_URL,
        credential.client_secret,
    )
