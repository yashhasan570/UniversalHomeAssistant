"""Provides conditions for gates."""

from universalassistant.components.cover import (
    DOMAIN as COVER_DOMAIN,
    CoverDeviceClass,
    make_cover_is_closed_condition,
    make_cover_is_open_condition,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.condition import Condition

DEVICE_CLASSES_GATE: dict[str, str] = {
    COVER_DOMAIN: CoverDeviceClass.GATE,
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_closed": make_cover_is_closed_condition(device_classes=DEVICE_CLASSES_GATE),
    "is_open": make_cover_is_open_condition(device_classes=DEVICE_CLASSES_GATE),
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the conditions for gates."""
    return CONDITIONS
