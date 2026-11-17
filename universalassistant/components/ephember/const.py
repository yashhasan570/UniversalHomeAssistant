"""Constants for the EPH Controls Ember integration."""

import logging
from typing import Final

from universalassistant.const import Platform

LOGGER = logging.getLogger(__package__)
DOMAIN: Final = "ephember"
PLATFORMS = [Platform.CLIMATE]
