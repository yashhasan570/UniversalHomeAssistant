"""Provides device automations for Arcam FMJ Receiver control."""

import probatio

from universalassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from universalassistant.components.media_player import DOMAIN as MEDIA_PLAYER_DOMAIN
from universalassistant.const import (
    ATTR_ENTITY_ID,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_PLATFORM,
    CONF_TYPE,
)
from universalassistant.core import (
    CALLBACK_TYPE,
    Event,
    HassJob,
    UniversalAssistant,
    async_noop,
    callback,
)
from universalassistant.helpers import config_validation as cv, entity_registry as er
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_TURN_ON

TRIGGER_TYPES = {"turn_on"}
TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        probatio.Required(CONF_ENTITY_ID): cv.entity_id_or_uuid,
        probatio.Required(CONF_TYPE): probatio.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(
    hass: UniversalAssistant, device_id: str
) -> list[dict[str, str]]:
    """List device triggers for Arcam FMJ Receiver control devices."""
    entity_registry = er.async_get(hass)

    return [
        {
            CONF_PLATFORM: "device",
            CONF_DEVICE_ID: device_id,
            CONF_DOMAIN: DOMAIN,
            CONF_ENTITY_ID: entry.id,
            CONF_TYPE: "turn_on",
        }
        for entry in er.async_entries_for_device(entity_registry, device_id)
        if entry.domain == MEDIA_PLAYER_DOMAIN
    ]


async def async_attach_trigger(
    hass: UniversalAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    trigger_data = trigger_info["trigger_data"]
    job = HassJob(action)

    if config[CONF_TYPE] == "turn_on":
        registry = er.async_get(hass)
        entity_id = er.async_resolve_entity_id(registry, config[ATTR_ENTITY_ID])

        @callback
        def _handle_event(event: Event) -> None:
            if event.data[ATTR_ENTITY_ID] == entity_id:
                hass.async_run_hass_job(
                    job,
                    {
                        "trigger": {
                            **trigger_data,
                            **config,
                            "description": f"{DOMAIN} - {entity_id}",
                            "entity_id": entity_id,
                        }
                    },
                    event.context,
                )

        return hass.bus.async_listen(EVENT_TURN_ON, _handle_event)

    return async_noop
