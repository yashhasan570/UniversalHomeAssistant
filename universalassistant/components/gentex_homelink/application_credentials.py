"""application_credentials platform for the gentex homelink integration."""

from universalassistant.components.application_credentials import ClientCredential
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_entry_oauth2_flow

from . import oauth2


async def async_get_auth_implementation(
    hass: UniversalAssistant, auth_domain: str, _credential: ClientCredential
) -> config_entry_oauth2_flow.AbstractOAuth2Implementation:
    """Return custom HomeLink OAuth2 implementation."""
    return oauth2.HomeLinkOAuth2Implementation(hass, auth_domain)
