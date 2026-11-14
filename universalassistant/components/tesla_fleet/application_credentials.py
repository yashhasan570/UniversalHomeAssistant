"""Application Credentials platform the Tesla Fleet integration."""

from universalassistant.components.application_credentials import ClientCredential
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_entry_oauth2_flow

from .oauth import TeslaUserImplementation


async def async_get_auth_implementation(
    hass: __HAC_KEEP__, auth_domain: str, credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return auth implementation."""
    return TeslaUserImplementation(
        hass,
        auth_domain,
        credential,
    )
