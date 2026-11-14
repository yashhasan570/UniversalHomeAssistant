"""Plugged In Status Support for the Nissan Leaf."""

import logging
from typing import override

from universalassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import LeafDataStore
from .const import DATA_CHARGING, DATA_LEAF, DATA_PLUGGED_IN
from .entity import LeafEntity

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: UniversalAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up of a Nissan Leaf binary sensor."""
    if discovery_info is None:
        return

    entities: list[LeafEntity] = []
    for vin, datastore in hass.data[DATA_LEAF].items():
        _LOGGER.debug("Adding binary_sensors for vin=%s", vin)
        entities.append(LeafPluggedInSensor(datastore))
        entities.append(LeafChargingSensor(datastore))

    add_entities(entities, True)


class LeafPluggedInSensor(LeafEntity, BinarySensorEntity):
    """Plugged In Sensor class."""

    _attr_device_class = BinarySensorDeviceClass.PLUG

    def __init__(self, car: LeafDataStore) -> None:
        """Set up plug status sensor."""
        super().__init__(car)
        self._attr_unique_id = f"{self.car.leaf.vin.lower()}_plugstatus"

    @property
    @override
    def name(self) -> str:
        """Sensor name."""
        return f"{self.car.leaf.nickname} Plug Status"

    @property
    @override
    def available(self) -> bool:
        """Sensor availability."""
        return self.car.data[DATA_PLUGGED_IN] is not None

    @property
    @override
    def is_on(self) -> bool:
        """Return true if plugged in."""
        return bool(self.car.data[DATA_PLUGGED_IN])


class LeafChargingSensor(LeafEntity, BinarySensorEntity):
    """Charging Sensor class."""

    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    def __init__(self, car: LeafDataStore) -> None:
        """Set up charging status sensor."""
        super().__init__(car)
        self._attr_unique_id = f"{self.car.leaf.vin.lower()}_chargingstatus"

    @property
    @override
    def name(self) -> str:
        """Sensor name."""
        return f"{self.car.leaf.nickname} Charging Status"

    @property
    @override
    def available(self) -> bool:
        """Sensor availability."""
        return self.car.data[DATA_CHARGING] is not None

    @property
    @override
    def is_on(self) -> bool:
        """Return true if charging."""
        return bool(self.car.data[DATA_CHARGING])
