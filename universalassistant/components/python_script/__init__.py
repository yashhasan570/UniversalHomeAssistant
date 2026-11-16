"""Component to allow running Python scripts."""

import logging
import os

import probatio

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN, FOLDER
from .services import discover_scripts, setup_services

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = probatio.Schema(
    {DOMAIN: probatio.Schema(dict)}, extra=probatio.ALLOW_EXTRA
)


def setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Initialize the Python script component."""
    setup_services(hass)

    path = hass.config.path(FOLDER)

    if not os.path.isdir(path):
        _LOGGER.warning("Folder %s not found in configuration folder", FOLDER)
        return False

    discover_scripts(hass)

    return True
