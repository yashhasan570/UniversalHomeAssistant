"""Provides conditions for windows."""

from universalassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
)
from universalassistant.components.cover import (
    DOMAIN as COVER_DOMAIN,
    CoverDeviceClass,
    make_cover_is_closed_condition,
    make_cover_is_open_condition,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.condition import Condition

DEVICE_CLASSES_WINDOW: dict[str, str] = {
    BINARY_SENSOR_DOMAIN: BinarySensorDeviceClass.WINDOW,
    COVER_DOMAIN: CoverDeviceClass.WINDOW,
}

CONDITIONS: dict[str, type[Condition]] = {
    "is_closed": make_cover_is_closed_condition(device_classes=DEVICE_CLASSES_WINDOW),
    "is_open": make_cover_is_open_condition(device_classes=DEVICE_CLASSES_WINDOW),
}


async def async_get_conditions(hass: __HAC_KEEP__) -> dict[str, type[Condition]]:
    """Return the conditions for windows."""
    return CONDITIONS
