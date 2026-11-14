"""Constants for the CPU Speed integration."""

import logging
from typing import Final

from universalassistant.const import Platform

DOMAIN: Final = "cpuspeed"
PLATFORMS = [Platform.SENSOR]

LOGGER = logging.getLogger(__package__)
