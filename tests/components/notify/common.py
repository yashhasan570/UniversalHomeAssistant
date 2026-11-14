"""Collection of helper methods.

All containing methods are legacy helpers that should not be used by new
components. Instead call the service directly.
"""

from typing import Any

from universalassistant.components.notify import (
    ATTR_DATA,
    ATTR_MESSAGE,
    ATTR_TITLE,
    DOMAIN,
    SERVICE_NOTIFY,
)
from universalassistant.core import UniversalAssistant


def send_message(
    hass: UniversalAssistant, message: str, title: str | None = None, data: Any = None
) -> None:
    """Send a notification message."""
    info = {ATTR_MESSAGE: message}

    if title is not None:
        info[ATTR_TITLE] = title

    if data is not None:
        info[ATTR_DATA] = data

    hass.services.call(DOMAIN, SERVICE_NOTIFY, info)
