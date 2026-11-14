"""Provide device triggers for KNX."""

from typing import Any, Final

import probatio

from universalassistant.components.device_automation import (
    DEVICE_TRIGGER_BASE_SCHEMA,
    InvalidDeviceAutomationConfig,
)
from universalassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from universalassistant.core import CALLBACK_TYPE, HassJob, __HAC_KEEP__, callback
from universalassistant.helpers import selector
from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, KNX_MODULE_KEY
from .trigger import (
    CONF_KNX_DESTINATION,
    CONF_KNX_GROUP_VALUE_READ,
    CONF_KNX_GROUP_VALUE_RESPONSE,
    CONF_KNX_GROUP_VALUE_WRITE,
    CONF_KNX_INCOMING,
    CONF_KNX_OUTGOING,
    TELEGRAM_TRIGGER_SCHEMA,
    async_subscribe_telegrams,
)

TRIGGER_TELEGRAM: Final = "telegram"

TRIGGER_SCHEMA: Final = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        probatio.Required(CONF_TYPE): TRIGGER_TELEGRAM,
        **TELEGRAM_TRIGGER_SCHEMA,
    }
)
_TELEGRAM_OPTIONS_SCHEMA: Final = probatio.Schema(TELEGRAM_TRIGGER_SCHEMA)


async def async_get_triggers(
    hass: __HAC_KEEP__, device_id: str
) -> list[dict[str, Any]]:
    """List device triggers for KNX devices."""
    triggers = []

    knx = hass.data[KNX_MODULE_KEY]
    if knx.interface_device.device.id == device_id:
        # Add trigger for KNX telegrams to interface device
        triggers.append(
            {
                # Default fields when initializing the trigger
                CONF_PLATFORM: "device",
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: device_id,
                CONF_TYPE: TRIGGER_TELEGRAM,
            }
        )

    return triggers


async def async_get_trigger_capabilities(
    hass: __HAC_KEEP__, config: ConfigType
) -> dict[str, probatio.Schema]:
    """List trigger capabilities."""
    project = hass.data[KNX_MODULE_KEY].project
    options = [
        selector.SelectOptionDict(value=ga.address, label=f"{ga.address} - {ga.name}")
        for ga in project.group_addresses.values()
    ]
    return {
        "extra_fields": probatio.Schema(
            {
                probatio.Optional(CONF_KNX_DESTINATION): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        mode=selector.SelectSelectorMode.DROPDOWN,
                        multiple=True,
                        custom_value=True,
                        options=options,
                    ),
                ),
                probatio.Optional(
                    CONF_KNX_GROUP_VALUE_WRITE, default=True
                ): selector.BooleanSelector(),
                probatio.Optional(
                    CONF_KNX_GROUP_VALUE_RESPONSE, default=True
                ): selector.BooleanSelector(),
                probatio.Optional(
                    CONF_KNX_GROUP_VALUE_READ, default=True
                ): selector.BooleanSelector(),
                probatio.Optional(
                    CONF_KNX_INCOMING, default=True
                ): selector.BooleanSelector(),
                probatio.Optional(
                    CONF_KNX_OUTGOING, default=True
                ): selector.BooleanSelector(),
            }
        )
    }


async def async_attach_trigger(
    hass: __HAC_KEEP__,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    # Remove device trigger specific fields
    telegram_options = {
        key: config[key] for key in (config.keys() & TELEGRAM_TRIGGER_SCHEMA.keys())
    }

    try:
        telegram_options = _TELEGRAM_OPTIONS_SCHEMA(telegram_options)
    except probatio.Invalid as err:
        raise InvalidDeviceAutomationConfig(
            translation_domain=DOMAIN,
            translation_key="device_trigger_invalid_config",
            translation_placeholders={"error": str(err)},
        ) from err

    job = HassJob(action, f"KNX device trigger {trigger_info}")
    trigger_data = trigger_info["trigger_data"]

    @callback
    def async_telegram_received(telegram_data: dict[str, Any]) -> None:
        """Run the action for a matching telegram."""
        hass.async_run_hass_job(job, {"trigger": {**trigger_data, **telegram_data}})

    return async_subscribe_telegrams(hass, telegram_options, async_telegram_received)
