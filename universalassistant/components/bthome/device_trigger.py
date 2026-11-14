"""Provides device triggers for BTHome BLE."""

from typing import TYPE_CHECKING, Any

import probatio

from universalassistant.components.device_automation import (
    DEVICE_TRIGGER_BASE_SCHEMA,
    InvalidDeviceAutomationConfig,
)
from universalassistant.components.universalassistant.triggers import event as event_trigger
from universalassistant.components.universalassistant.triggers.event import EventTriggerArgument
from universalassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_EVENT,
    CONF_PLATFORM,
    CONF_TYPE,
)
from universalassistant.core import CALLBACK_TYPE, __HAC_KEEP__
from universalassistant.helpers import device_registry as dr
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from .const import (
    BTHOME_BLE_EVENT,
    CONF_DISCOVERED_EVENT_CLASSES,
    CONF_SUBTYPE,
    DOMAIN,
    EVENT_CLASS,
    EVENT_CLASS_BUTTON,
    EVENT_CLASS_COMMAND,
    EVENT_CLASS_DIMMER,
    EVENT_TYPE,
)

EVENT_TYPES_BY_EVENT_CLASS = {
    EVENT_CLASS_BUTTON: {
        "press",
        "double_press",
        "triple_press",
        "long_press",
        "long_double_press",
        "long_triple_press",
        "hold_press",
        "hold_release",
    },
    EVENT_CLASS_DIMMER: {"rotate_left", "rotate_right"},
    EVENT_CLASS_COMMAND: {"off", "on", "toggle", "step_up", "step_down"},
}

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {probatio.Required(CONF_TYPE): str, probatio.Required(CONF_SUBTYPE): str}
)


def get_event_classes_by_device_id(hass: __HAC_KEEP__, device_id: str) -> list[str]:
    """Get the supported event classes for a device.

    Events for BTHome BLE devices are dynamically discovered
    and stored in the device config entry when they are first seen.
    """
    _, config_entry = dr.async_get_device_and_config_entry_for_domain(
        hass, device_id, domain=DOMAIN
    )
    if TYPE_CHECKING:
        assert config_entry is not None
    return config_entry.data.get(CONF_DISCOVERED_EVENT_CLASSES, [])  # type: ignore[no-any-return]


def get_event_types_by_event_class(event_class: str) -> set[str]:
    """Get the supported event types for an event class.

    If the device has multiple buttons they will have
    event classes like button_1 button_2, button_3, etc
    but if there is only one button then it will be
    button without a number postfix.
    """
    return EVENT_TYPES_BY_EVENT_CLASS.get(event_class.split("_", maxsplit=1)[0], set())


async def async_validate_trigger_config(
    hass: __HAC_KEEP__, config: ConfigType
) -> ConfigType:
    """Validate trigger config."""
    config = TRIGGER_SCHEMA(config)
    event_class = config[CONF_TYPE]
    event_type = config[CONF_SUBTYPE]
    device_id = config[CONF_DEVICE_ID]
    event_classes = get_event_classes_by_device_id(hass, device_id)

    if event_class not in event_classes:
        raise InvalidDeviceAutomationConfig(
            f"BTHome trigger {event_class} is not valid for device_id '{device_id}'"
        )

    if event_type not in get_event_types_by_event_class(event_class):
        raise InvalidDeviceAutomationConfig(
            f"BTHome trigger {event_type} is not valid for device_id '{device_id}'"
        )

    return config


async def async_get_triggers(
    hass: __HAC_KEEP__, device_id: str
) -> list[dict[str, Any]]:
    """Return a list of triggers for BTHome BLE devices."""
    event_classes = get_event_classes_by_device_id(hass, device_id)
    return [
        {
            # Required fields of TRIGGER_BASE_SCHEMA
            CONF_PLATFORM: "device",
            CONF_DEVICE_ID: device_id,
            CONF_DOMAIN: DOMAIN,
            # Required fields of TRIGGER_SCHEMA
            CONF_TYPE: event_class,
            CONF_SUBTYPE: event_type,
        }
        for event_class in event_classes
        for event_type in get_event_types_by_event_class(event_class)
    ]


async def async_attach_trigger(
    hass: __HAC_KEEP__,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    return await event_trigger.async_attach_trigger(
        hass,
        event_trigger.TRIGGER_SCHEMA(
            {
                EventTriggerArgument.PLATFORM: CONF_EVENT,
                EventTriggerArgument.EVENT_TYPE: BTHOME_BLE_EVENT,
                EventTriggerArgument.EVENT_DATA: {
                    CONF_DEVICE_ID: config[CONF_DEVICE_ID],
                    EVENT_CLASS: config[CONF_TYPE],
                    EVENT_TYPE: config[CONF_SUBTYPE],
                },
            }
        ),
        action,
        trigger_info,
        platform_type="device",
    )
