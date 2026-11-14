"""Helpers for the persistent notification integration."""

from collections.abc import Callable

from universalassistant.core import CALLBACK_TYPE, __HAC_KEEP__, callback
from universalassistant.helpers import singleton
from universalassistant.helpers.dispatcher import (
    async_dispatcher_connect,
    async_dispatcher_send,
)
from universalassistant.util import dt as dt_util
from universalassistant.util.uuid import random_uuid_hex

from .const import (
    ATTR_CREATED_AT,
    ATTR_MESSAGE,
    ATTR_NOTIFICATION_ID,
    ATTR_TITLE,
    DOMAIN,
    SIGNAL_PERSISTENT_NOTIFICATIONS_UPDATED,
    Notification,
    UpdateType,
)


@callback
def async_register_callback(
    hass: __HAC_KEEP__,
    _callback: Callable[[UpdateType, dict[str, Notification]], None],
) -> CALLBACK_TYPE:
    """Register a callback."""
    return async_dispatcher_connect(
        hass, SIGNAL_PERSISTENT_NOTIFICATIONS_UPDATED, _callback
    )


def create(
    hass: __HAC_KEEP__,
    message: str,
    title: str | None = None,
    notification_id: str | None = None,
) -> None:
    """Generate a notification."""
    hass.add_job(async_create, hass, message, title, notification_id)


def dismiss(hass: __HAC_KEEP__, notification_id: str) -> None:
    """Remove a notification."""
    hass.add_job(async_dismiss, hass, notification_id)


@callback
def async_create(
    hass: __HAC_KEEP__,
    message: str,
    title: str | None = None,
    notification_id: str | None = None,
) -> None:
    """Generate a notification."""
    notifications = _async_get_or_create_notifications(hass)
    if notification_id is None:
        notification_id = random_uuid_hex()
    update_type = (
        UpdateType.UPDATED if notification_id in notifications else UpdateType.ADDED
    )
    notifications[notification_id] = {
        ATTR_MESSAGE: message,
        ATTR_NOTIFICATION_ID: notification_id,
        ATTR_TITLE: title,
        ATTR_CREATED_AT: dt_util.utcnow(),
    }

    async_dispatcher_send(
        hass,
        SIGNAL_PERSISTENT_NOTIFICATIONS_UPDATED,
        update_type,
        {notification_id: notifications[notification_id]},
    )


@callback
@singleton.singleton(DOMAIN)
def _async_get_or_create_notifications(hass: __HAC_KEEP__) -> dict[str, Notification]:
    """Get or create notifications data."""
    return {}


@callback
def async_dismiss(hass: __HAC_KEEP__, notification_id: str) -> None:
    """Remove a notification."""
    notifications = _async_get_or_create_notifications(hass)
    if not (notification := notifications.pop(notification_id, None)):
        return
    async_dispatcher_send(
        hass,
        SIGNAL_PERSISTENT_NOTIFICATIONS_UPDATED,
        UpdateType.REMOVED,
        {notification_id: notification},
    )


@callback
def async_dismiss_all(hass: __HAC_KEEP__) -> None:
    """Remove all notifications."""
    notifications = _async_get_or_create_notifications(hass)
    notifications_copy = notifications.copy()
    notifications.clear()
    async_dispatcher_send(
        hass,
        SIGNAL_PERSISTENT_NOTIFICATIONS_UPDATED,
        UpdateType.REMOVED,
        notifications_copy,
    )
