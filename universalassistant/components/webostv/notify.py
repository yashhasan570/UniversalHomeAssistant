"""Support for LG webOS TV notification service."""

from typing import Any, override

from aiowebostv import WebOsClient

from universalassistant.components.notify import ATTR_DATA, BaseNotificationService
from universalassistant.const import ATTR_CONFIG_ENTRY_ID
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import ATTR_ICON, DOMAIN, WEBOSTV_EXCEPTIONS
from .coordinator import WebOsTvConfigEntry

PARALLEL_UPDATES = 0


async def async_get_service(
    hass: UniversalAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> BaseNotificationService | None:
    """Return the notify service."""

    if discovery_info is None:
        return None

    config_entry = hass.config_entries.async_get_entry(
        discovery_info[ATTR_CONFIG_ENTRY_ID]
    )
    assert config_entry is not None

    return LgWebOSNotificationService(config_entry)


class LgWebOSNotificationService(BaseNotificationService):
    """Implement the notification service for LG webOS TV."""

    def __init__(self, entry: WebOsTvConfigEntry) -> None:
        """Initialize the service."""
        self._entry = entry

    @override
    async def async_send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send a message to the tv."""
        client: WebOsClient = self._entry.runtime_data.client
        data = kwargs[ATTR_DATA]
        icon_path = data.get(ATTR_ICON) if data else None

        if not client.tv_state.is_on:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="notify_device_off",
                translation_placeholders={"name": str(self._entry.title)},
            )
        try:
            await client.send_message(message, icon_path=icon_path)
        except FileNotFoundError as error:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="notify_icon_not_found",
                translation_placeholders={
                    "name": str(self._entry.title),
                    "icon_path": str(icon_path),
                },
            ) from error
        except WEBOSTV_EXCEPTIONS as error:
            raise UniversalAssistantError(
                translation_domain=DOMAIN,
                translation_key="notify_communication_error",
                translation_placeholders={
                    "name": str(self._entry.title),
                    "error": str(error),
                },
            ) from error
