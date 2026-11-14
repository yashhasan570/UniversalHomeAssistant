"""Application Credentials platform the Tesla Fleet integration."""

from universalassistant.components.application_credentials import ClientCredential
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_entry_oauth2_flow

from .oauth import TeslaUserImplementation


async def async_get_auth_implementation(
    hass: UniversalAssistant, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return TeslaUserImplementation(
        hass,
        auth_domain,
        credential,
    )
