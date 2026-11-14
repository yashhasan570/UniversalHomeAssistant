"""Provide oauth implementations for the Tesla Fleet integration."""

from typing import Any, override

from universalassistant.components.application_credentials import (
    AuthImplementation,
    AuthorizationServer,
    ClientCredential,
)
from universalassistant.core import __HAC_KEEP__

from .const import AUTHORIZE_URL, SCOPES, TOKEN_URL


class TeslaUserImplementation(AuthImplementation):
    """Tesla Fleet API user Oauth2 implementation."""

    def __init__(
        self, hass: __HAC_KEEP__, auth_domain: str, credential: ClientCredential
    ) -> None:
        """Initialize user Oauth2 implementation."""

        super().__init__(
            hass,
            auth_domain,
            credential,
            AuthorizationServer(AUTHORIZE_URL, TOKEN_URL),
        )

    @property
    @override
    def extra_authorize_data(self) -> dict[str, Any]:
        """Extra data that needs to be appended to the authorize url."""
        return {
            "prompt": "login",
            "prompt_missing_scopes": "true",
            "scope": " ".join(SCOPES),
        }
