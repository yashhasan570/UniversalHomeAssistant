"""Constants for Discogs."""

import logging
from typing import Final

from universalassistant.const import Platform

LOGGER = logging.getLogger(__package__)
DOMAIN: Final = "discogs"
PLATFORMS = [Platform.SENSOR]
DEFAULT_NAME = "Discogs"
