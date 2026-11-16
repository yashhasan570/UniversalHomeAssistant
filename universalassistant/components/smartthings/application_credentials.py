"""Application credentials platform for SmartThings."""

from universalassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.config_entry_oauth2_flow import AbstractOAuth2Implementation

from .const import DOMAIN


async def async_get_auth_implementation(
    hass: UniversalAssistant, auth_domain: str, credential: ClientCredential
) -> AbstractOAuth2Implementation:
    """Return auth implementation."""
    return SmartThingsOAuth2Implementation(
        hass,
        DOMAIN,
        credential,
        authorization_server=AuthorizationServer(
            authorize_url="https://api.smartthings.com/oauth/authorize",
            token_url="https://auth-global.api.smartthings.com/oauth/token",
        ),
    )


class SmartThingsOAuth2Implementation(AuthImplementation):
    """Oauth2 implementation that only uses the external url."""

    token_auth_method = "client_secret_basic"
