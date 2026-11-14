"""Charge and Climate Control Support for the Nissan Leaf."""

import logging
from typing import Any, override

from universalassistant.components.switch import SwitchEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import LeafDataStore
from .const import DATA_CLIMATE, DATA_LEAF
from .entity import LeafEntity

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: __HAC_KEEP__,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Nissan Leaf switch platform setup."""
    if discovery_info is None:
        return

    entities: list[LeafEntity] = []
    for vin, datastore in hass.data[DATA_LEAF].items():
        _LOGGER.debug("Adding switch for vin=%s", vin)
        entities.append(LeafClimateSwitch(datastore))

    add_entities(entities, True)


class LeafClimateSwitch(LeafEntity, SwitchEntity):
    """Nissan Leaf Climate Control switch."""

    def __init__(self, car: LeafDataStore) -> None:
        """Set up climate control switch."""
        super().__init__(car)
        self._attr_unique_id = f"{self.car.leaf.vin.lower()}_climatecontrol"

    @property
    @override
    def name(self) -> str:
        """Switch name."""
        return f"{self.car.leaf.nickname} Climate Control"

    @override
    def log_registration(self) -> None:
        """Log registration."""
        _LOGGER.debug(
            "Registered LeafClimateSwitch integration with __HA_KEEP__ for VIN %s",
            self.car.leaf.vin,
        )

    @property
    @override
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return climate control attributes."""
        attrs = super().extra_state_attributes
        attrs["updated_on"] = self.car.last_climate_response
        return attrs

    @property
    @override
    def is_on(self) -> bool:
        """Return true if climate control is on."""
        return bool(self.car.data[DATA_CLIMATE])

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on climate control."""
        if await self.car.async_set_climate(True):
            self.car.data[DATA_CLIMATE] = True

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn off climate control."""
        if await self.car.async_set_climate(False):
            self.car.data[DATA_CLIMATE] = False
