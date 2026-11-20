"""Support for Ambient Weather Network sensors."""

from datetime import datetime
from typing import override

from universalassistant.components.sensor import SensorDeviceClass, SensorEntity
from universalassistant.const import CONF_MAC
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from universalassistant.util import dt as dt_util

from .const import SENSOR_DESCRIPTIONS
from .coordinator import AmbientNetworkConfigEntry
from .entity import AmbientNetworkEntity


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: AmbientNetworkConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Ambient Network sensor entities."""

    coordinator = entry.runtime_data
    if coordinator.config_entry is not None:
        async_add_entities(
            AmbientNetworkSensor(
                coordinator,
                description,
                coordinator.config_entry.data[CONF_MAC],
            )
            for description in SENSOR_DESCRIPTIONS
            if coordinator.data.get(description.key) is not None
        )


class AmbientNetworkSensor(AmbientNetworkEntity, SensorEntity):
    """A sensor implementation for an Ambient Weather Network sensor."""

    @override
    def _update_attrs(self) -> None:
        """Update sensor attributes."""
        value = self.coordinator.data.get(self.entity_description.key)

        # Treatments for special units.
        if value is not None and self.device_class == SensorDeviceClass.TIMESTAMP:
            value = datetime.fromtimestamp(
                value / 1000, tz=dt_util.get_default_time_zone()
            )

        self._attr_available = value is not None
        self._attr_native_value = value

        if self.coordinator.last_measured is not None:
            self._attr_extra_state_attributes = {
                "last_measured": self.coordinator.last_measured
            }
