"""Threema Gateway API client, wired to __HA_KEEP__'s shared aiohttp session."""

from aiothreema import (
    ThreemaAuthError,
    ThreemaConnectionError,
    ThreemaGatewayClient,
    ThreemaNoCreditsError,
    ThreemaRateLimitError,
    ThreemaSendError,
    derive_public_key,
    generate_key_pair,
)

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.aiohttp_client import async_get_clientsession

__all__ = [
    "ThreemaAPIClient",
    "ThreemaAuthError",
    "ThreemaConnectionError",
    "ThreemaNoCreditsError",
    "ThreemaRateLimitError",
    "ThreemaSendError",
    "derive_public_key",
    "generate_key_pair",
]


class ThreemaAPIClient(ThreemaGatewayClient):
    """Threema Gateway client bound to __HA_KEEP__'s shared aiohttp session.

    The Gateway HTTP protocol and end-to-end encryption live in the
    `aiothreema` library; this class only wires it up to __HA_KEEP__.
    """

    def __init__(
        self,
        hass: __HAC_KEEP__,
        gateway_id: str,
        api_secret: str,
        private_key: str | None = None,
    ) -> None:
        """Initialize the client with __HA_KEEP__'s shared session."""
        super().__init__(
            gateway_id,
            api_secret,
            private_key,
            session=async_get_clientsession(hass),
        )
