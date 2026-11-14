"""application_credentials platform the Electric Kiwi integration."""

from universalassistant.components.application_credentials import (
    AuthorizationServer,
    ClientCredential,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_entry_oauth2_flow

from .const import OAUTH2_AUTHORIZE, OAUTH2_TOKEN
from .oauth2 import ElectricKiwiLocalOAuth2Implementation


async def async_get_auth_implementation(
    hass: __HAC_KEEP__, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return ElectricKiwiLocalOAuth2Implementation(
        hass,
        auth_domain,
        credential,
        authorization_server=await async_get_authorization_server(hass),
    )


async def async_get_authorization_server(hass: __HAC_KEEP__) -> AuthorizationServer:
    """Return authorization server."""
    return AuthorizationServer(
        authorize_url=OAUTH2_AUTHORIZE,
        token_url=OAUTH2_TOKEN,
    )


async def async_get_description_placeholders(hass: __HAC_KEEP__) -> dict[str, str]:
    """Return description placeholders for the credentials dialog."""
    return {
        "more_info_url": "https://www.universalassistant.io/integrations/electric_kiwi/"
    }
