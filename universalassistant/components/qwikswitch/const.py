"""Support for Qwikswitch devices."""

from typing import TYPE_CHECKING

from universalassistant.util.hass_dict import HassKey

if TYPE_CHECKING:
    from pyqwikswitch.async_ import QSUsb

DOMAIN = "qwikswitch"
DATA_QUIKSWITCH: HassKey[QSUsb] = HassKey(DOMAIN)
