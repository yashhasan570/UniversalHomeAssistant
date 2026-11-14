"""Constants for the iNELS integration."""

import logging

from universalassistant.const import Platform

DOMAIN = "inels"
TITLE = "iNELS"

PLATFORMS: list[Platform] = [
    Platform.SWITCH,
]

LOGGER = logging.getLogger(__package__)
