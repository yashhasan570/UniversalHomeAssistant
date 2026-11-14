"""Support for Qwikswitch relays."""

from universalassistant.components.switch import SwitchEntity
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import DATA_QUIKSWITCH, DOMAIN
from .entity import QSToggleEntity


async def async_setup_platform(
    hass: __HAC_KEEP__,
    _: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Add switches from the main Qwikswitch component."""
    if discovery_info is None:
        return

    qsusb = hass.data[DATA_QUIKSWITCH]
    devs = [QSSwitch(qsid, qsusb) for qsid in discovery_info[DOMAIN]]
    add_entities(devs)


class QSSwitch(QSToggleEntity, SwitchEntity):
    """Switch based on a Qwikswitch relay module."""
