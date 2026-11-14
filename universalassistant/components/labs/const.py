"""Constants for the __HA_KEEP__ Labs integration."""

from universalassistant.util.hass_dict import HassKey

from .models import LabsData

DOMAIN = "labs"

STORAGE_KEY = "core.labs"
STORAGE_VERSION = 1

LABS_DATA: HassKey[LabsData] = HassKey(DOMAIN)
