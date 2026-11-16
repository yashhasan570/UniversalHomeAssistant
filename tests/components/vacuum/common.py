"""Collection of helper methods.

All containing methods are legacy helpers that should not be used by new
components. Instead call the service directly.
"""

from typing import Any

from universalassistant.components.vacuum import (
    ATTR_FAN_SPEED,
    ATTR_PARAMS,
    DOMAIN,
    SERVICE_CLEAN_AREA,
    SERVICE_CLEAN_SPOT,
    SERVICE_LOCATE,
    SERVICE_PAUSE,
    SERVICE_RETURN_TO_BASE,
    SERVICE_SEND_COMMAND,
    SERVICE_SET_FAN_SPEED,
    SERVICE_START,
    SERVICE_STOP,
)
from universalassistant.const import (
    ATTR_COMMAND,
    ATTR_ENTITY_ID,
    ENTITY_MATCH_ALL,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
from universalassistant.core import UniversalAssistant


async def async_turn_on(hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Turn all or specified vacuum on."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_TURN_ON, data, blocking=True)


async def async_turn_off(
    hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL
) -> None:
    """Turn all or specified vacuum off."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_TURN_OFF, data, blocking=True)


async def async_toggle(hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Toggle all or specified vacuum."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_TOGGLE, data, blocking=True)


async def async_locate(hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Locate all or specified vacuum."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_LOCATE, data, blocking=True)


async def async_clean_area(
    hass: UniversalAssistant,
    cleaning_area_id: list[str],
    entity_id: str = ENTITY_MATCH_ALL,
) -> None:
    """Tell all or specified vacuum to perform an area clean."""
    data = {"cleaning_area_id": cleaning_area_id}
    if entity_id:
        data[ATTR_ENTITY_ID] = entity_id
    await hass.services.async_call(DOMAIN, SERVICE_CLEAN_AREA, data, blocking=True)


async def async_clean_spot(
    hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL
) -> None:
    """Tell all or specified vacuum to perform a spot clean-up."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_CLEAN_SPOT, data, blocking=True)


async def async_return_to_base(
    hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL
) -> None:
    """Tell all or specified vacuum to return to base."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_RETURN_TO_BASE, data, blocking=True)


async def async_start(hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Tell all or specified vacuum to start or resume the current task."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_START, data, blocking=True)


async def async_pause(hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Tell all or the specified vacuum to pause the current task."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_PAUSE, data, blocking=True)


async def async_stop(hass: UniversalAssistant, entity_id: str = ENTITY_MATCH_ALL) -> None:
    """Stop all or specified vacuum."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else None
    await hass.services.async_call(DOMAIN, SERVICE_STOP, data, blocking=True)


async def async_set_fan_speed(
    hass: UniversalAssistant, fan_speed: str, entity_id: str = ENTITY_MATCH_ALL
) -> None:
    """Set fan speed for all or specified vacuum."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    data[ATTR_FAN_SPEED] = fan_speed
    await hass.services.async_call(DOMAIN, SERVICE_SET_FAN_SPEED, data, blocking=True)


async def async_send_command(
    hass: UniversalAssistant,
    command: str,
    params: dict[str, Any] | list[Any] | None = None,
    entity_id: str = ENTITY_MATCH_ALL,
) -> None:
    """Send command to all or specified vacuum."""
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}
    data[ATTR_COMMAND] = command
    if params is not None:
        data[ATTR_PARAMS] = params
    await hass.services.async_call(DOMAIN, SERVICE_SEND_COMMAND, data, blocking=True)
