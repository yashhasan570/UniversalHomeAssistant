"""Application credentials platform for the Volvo integration."""

from typing import override

from volvocarsapi.auth import AUTHORIZE_URL, TOKEN_URL
from volvocarsapi.scopes import ALL_SCOPES

from universalassistant.components.application_credentials import ClientCredential
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.config_entry_oauth2_flow import (
    LocalOAuth2ImplementationWithPkce,
)


async def async_get_auth_implementation(
    hass: UniversalAssistant, auth_domain: str, credential: ClientCredential
) -> VolvoOAuth2Implementation:
    """Return auth implementation for a custom auth implementation."""
    return VolvoOAuth2Implementation(
        hass,
        auth_domain,
        credential.client_id,
        AUTHORIZE_URL,
        TOKEN_URL,
        credential.client_secret,
    )


class VolvoOAuth2Implementation(LocalOAuth2ImplementationWithPkce):
    """Volvo oauth2 implementation."""

    @property
    @override
    def extra_authorize_data(self) -> dict:
        """Extra data that needs to be appended to the authorize url."""
        return super().extra_authorize_data | {
            "scope": " ".join(ALL_SCOPES),
        }
