"""Provides device automations for Philips Hue events."""

import logging
from typing import TYPE_CHECKING, Any

from universalassistant.components.device_automation import InvalidDeviceAutomationConfig
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_DEVICE_ID
from universalassistant.core import CALLBACK_TYPE, callback
from universalassistant.helpers import device_registry as dr
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .v1.device_trigger import (
    async_attach_trigger as async_attach_trigger_v1,
    async_get_triggers as async_get_triggers_v1,
    async_validate_trigger_config as async_validate_trigger_config_v1,
)
from .v2.device_trigger import (
    async_attach_trigger as async_attach_trigger_v2,
    async_get_triggers as async_get_triggers_v2,
    async_validate_trigger_config as async_validate_trigger_config_v2,
)

if TYPE_CHECKING:
    from universalassistant.core import UniversalAssistant
    from universalassistant.helpers.trigger import TriggerActionType, TriggerInfo

    from .bridge import HueConfigEntry

LOGGER = logging.getLogger(__name__)


async def async_validate_trigger_config(
    hass: UniversalAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    entries: list[HueConfigEntry] = hass.config_entries.async_loaded_entries(DOMAIN)
    if not entries:
        # happens at startup
        return config
    device_id = config[CONF_DEVICE_ID]
    # lookup device in HASS DeviceRegistry
    dev_reg: dr.DeviceRegistry = dr.async_get(hass)
    if (
        device_entry := dev_reg.async_get(device_id, include_child_devices=False)
    ) is None:
        raise InvalidDeviceAutomationConfig(f"Device ID {device_id} is not valid")

    entry_ids = _device_config_entry_ids(device_entry)
    for entry in entries:
        if entry.entry_id not in entry_ids:
            continue
        bridge = entry.runtime_data
        if bridge.api_version == 1:
            return await async_validate_trigger_config_v1(bridge, device_entry, config)
        return await async_validate_trigger_config_v2(bridge, device_entry, config)
    return config


async def async_attach_trigger(
    hass: UniversalAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Listen for state changes based on configuration."""
    device_id = config[CONF_DEVICE_ID]
    # lookup device in HASS DeviceRegistry
    dev_reg: dr.DeviceRegistry = dr.async_get(hass)
    if (
        device_entry := dev_reg.async_get(device_id, include_child_devices=False)
    ) is None:
        raise InvalidDeviceAutomationConfig(f"Device ID {device_id} is not valid")

    entry_ids = _device_config_entry_ids(device_entry)
    entry: HueConfigEntry | None = next(
        (
            entry
            for entry in hass.config_entries.async_entries(DOMAIN)
            if entry.entry_id in entry_ids
        ),
        None,
    )
    if entry is None:
        raise InvalidDeviceAutomationConfig(
            f"Device ID {device_id} is not found on any Hue bridge"
        )

    if entry.state is not ConfigEntryState.LOADED:
        # The bridge is still setting up when automations are attached at startup.
        return _async_attach_on_entry_load(
            hass, entry, device_entry, config, action, trigger_info
        )

    return await _async_attach_bridge_trigger(
        entry, device_entry, config, action, trigger_info
    )


async def async_get_triggers(
    hass: UniversalAssistant, device_id: str
) -> list[dict[str, Any]]:
    """Get device triggers for given (hass) device id."""
    entries: list[HueConfigEntry] = hass.config_entries.async_loaded_entries(DOMAIN)
    if not entries:
        return []
    # lookup device in HASS DeviceRegistry
    dev_reg: dr.DeviceRegistry = dr.async_get(hass)
    if (
        device_entry := dev_reg.async_get(device_id, include_child_devices=False)
    ) is None:
        raise ValueError(f"Device ID {device_id} is not valid")

    # Iterate all config entries for this device
    # and work out the bridge version
    entry_ids = _device_config_entry_ids(device_entry)
    for entry in entries:
        if entry.entry_id not in entry_ids:
            continue
        bridge = entry.runtime_data

        if bridge.api_version == 1:
            return async_get_triggers_v1(bridge, device_entry)
        return async_get_triggers_v2(bridge, device_entry)
    return []


def _device_config_entry_ids(device_entry: dr.DeviceEntry) -> set[str]:
    """Return the ids of the config entries the device belongs to.

    A restored composite has no single owning config entry; the union of the
    split devices' config entries covers every owning domain.
    """
    if device_entry.is_composite_device:
        return device_entry.config_entries
    return {device_entry.config_entry_id}


async def _async_attach_bridge_trigger(
    entry: HueConfigEntry,
    device_entry: dr.DeviceEntry,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach the trigger to the bridge of a loaded config entry."""
    bridge = entry.runtime_data
    if bridge.api_version == 1:
        return await async_attach_trigger_v1(
            bridge, device_entry, config, action, trigger_info
        )
    return await async_attach_trigger_v2(
        bridge, device_entry, config, action, trigger_info
    )


@callback
def _async_attach_on_entry_load(
    hass: UniversalAssistant,
    entry: HueConfigEntry,
    device_entry: dr.DeviceEntry,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach the trigger as soon as the given config entry is loaded.

    The returned callback detaches the trigger and is safe to call while the
    config entry is still loading.
    """
    remove_trigger: CALLBACK_TYPE | None = None
    attach_scheduled = False

    async def _async_attach() -> None:
        nonlocal remove_trigger
        try:
            remove_trigger = await _async_attach_bridge_trigger(
                entry, device_entry, config, action, trigger_info
            )
        except InvalidDeviceAutomationConfig as err:
            LOGGER.error(
                "Got error '%s' when setting up triggers for %s",
                err,
                trigger_info["name"],
            )

    @callback
    def _handle_entry_state_change() -> None:
        nonlocal attach_scheduled
        # Unsubscribing here would mutate the list this callback is iterated from,
        # so the subscription is kept until the trigger is detached.
        if attach_scheduled or entry.state is not ConfigEntryState.LOADED:
            return
        attach_scheduled = True
        hass.async_create_task(_async_attach())

    unsub_state_change = entry.async_on_state_change(_handle_entry_state_change)

    @callback
    def _remove() -> None:
        unsub_state_change()
        if remove_trigger is not None:
            remove_trigger()

    return _remove
