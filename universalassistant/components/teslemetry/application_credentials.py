"""Application Credentials platform the Teslemetry integration."""

from universalassistant.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_entry_oauth2_flow

from .const import AUTHORIZE_URL, TOKEN_URL
from .oauth import TeslemetryImplementation


async def async_get_authorization_server(hass: UniversalAssistant) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=AUTHORIZE_URL,
        token_url=TOKEN_URL,
    )


async def async_get_auth_implementation(
    hass: UniversalAssistant, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return TeslemetryImplementation(
        hass,
        auth_domain,
        credential.client_id,
    )
