"""Consts used by profiler."""

from universalassistant.core import CALLBACK_TYPE
from universalassistant.util.hass_dict import HassKey

DOMAIN = "profiler"
DATA_PROFILER: HassKey[dict[str, CALLBACK_TYPE]] = HassKey(DOMAIN)
DEFAULT_NAME = "Profiler"
