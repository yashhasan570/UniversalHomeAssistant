"""Constants for the systemnexa2 integration."""

from typing import Final

from universalassistant.const import Platform

DOMAIN = "systemnexa2"
MANUFACTURER = "NEXA"
PLATFORMS: Final = [Platform.LIGHT, Platform.SENSOR, Platform.SWITCH]
