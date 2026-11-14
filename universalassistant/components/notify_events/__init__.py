"""The notify_events component."""

import probatio

from universalassistant.const import CONF_TOKEN, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv, discovery
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN

CONFIG_SCHEMA = probatio.Schema(
    {
        DOMAIN: probatio.Schema(
            {probatio.Required(probatio.Secret(CONF_TOKEN)): cv.string}
        )
    },
    extra=probatio.ALLOW_EXTRA,
)


def setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Set up the notify_events component."""

    hass.data[DOMAIN] = config[DOMAIN]
    discovery.load_platform(hass, Platform.NOTIFY, DOMAIN, {}, config)
    return True
