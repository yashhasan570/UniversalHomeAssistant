"""Support for showing the time in a different time zone."""

from datetime import tzinfo

from universalassistant.components.sensor import SensorEntity
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import CONF_TIME_ZONE
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.util import dt as dt_util

from .const import CONF_TIME_FORMAT, DOMAIN


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the World clock sensor entry."""
    time_zone = await dt_util.async_get_time_zone(entry.options[CONF_TIME_ZONE])
    async_add_entities(
        [
            WorldClockSensor(
                time_zone,
                entry.title,
                entry.options[CONF_TIME_FORMAT],
                entry.entry_id,
            )
        ],
        True,
    )


class WorldClockSensor(SensorEntity):
    """Representation of a World clock sensor."""

    _attr_icon = "mdi:clock"
    _attr_has_entity_name = True
    _attr_name = None

    def __init__(
        self, time_zone: tzinfo | None, name: str, time_format: str, unique_id: str
    ) -> None:
        """Initialize the sensor."""
        self._time_zone = time_zone
        self._time_format = time_format
        self._attr_unique_id = unique_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, unique_id)},
            name=name,
            entry_type=DeviceEntryType.SERVICE,
            manufacturer="Worldclock",
        )

    async def async_update(self) -> None:
        """Get the time and updates the states."""
        self._attr_native_value = dt_util.now(time_zone=self._time_zone).strftime(
            self._time_format
        )
