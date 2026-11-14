"""The Elv integration."""

import probatio

from universalassistant.const import CONF_DEVICE, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv, discovery
from universalassistant.helpers.typing import ConfigType

DOMAIN = "elv"

DEFAULT_DEVICE = "/dev/ttyUSB0"

ELV_PLATFORMS = [Platform.SWITCH]

CONFIG_SCHEMA = probatio.Schema(
    {
        DOMAIN: probatio.Schema(
            {probatio.Optional(CONF_DEVICE, default=DEFAULT_DEVICE): cv.string}
        )
    },
    extra=probatio.ALLOW_EXTRA,
)


def setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the PCA switch platform."""

    for platform in ELV_PLATFORMS:
        discovery.load_platform(
            hass, platform, DOMAIN, {"device": config[DOMAIN][CONF_DEVICE]}, config
        )

    return True
