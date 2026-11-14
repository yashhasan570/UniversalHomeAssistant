"""Flock platform for notify component."""

import asyncio
from http import HTTPStatus
import logging
from typing import Any, override

import aiohttp
import probatio

from universalassistant.components.notify import (
    PLATFORM_SCHEMA as NOTIFY_PLATFORM_SCHEMA,
    BaseNotificationService,
)
from universalassistant.const import CONF_ACCESS_TOKEN
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

DOMAIN = "flock"

_LOGGER = logging.getLogger(__name__)
_RESOURCE = "https://api.flock.com/hooks/sendMessage/"

PLATFORM_SCHEMA = NOTIFY_PLATFORM_SCHEMA.extend(
    {probatio.Required(probatio.Secret(CONF_ACCESS_TOKEN)): cv.string}
)


async def async_get_service(
    hass: UniversalAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> FlockNotificationService:
    """Get the Flock notification service."""
    access_token = config.get(CONF_ACCESS_TOKEN)
    url = f"{_RESOURCE}{access_token}"
    session = async_get_clientsession(hass)

    return FlockNotificationService(url, session)


class FlockNotificationService(BaseNotificationService):
    """Implement the notification service for Flock."""

    def __init__(self, url, session):
        """Initialize the Flock notification service."""
        self._url = url
        self._session = session

    @override
    async def async_send_message(self, message: str, **kwargs: Any) -> None:
        """Send the message to the user."""
        payload = {"text": message}

        _LOGGER.debug("Attempting to call Flock at %s", self._url)

        try:
            async with asyncio.timeout(10):
                response = await self._session.post(self._url, json=payload)
                result = await response.json()
        except TimeoutError as err:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="timeout",
            ) from err
        except aiohttp.ClientError as err:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="send_message_failed",
            ) from err

        if response.status != HTTPStatus.OK or "error" in result:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="send_message_failed",
            )
