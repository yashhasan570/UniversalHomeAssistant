"""Support for Melissa climate."""

from melissa import AsyncMelissa
import probatio

from universalassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.discovery import async_load_platform
from universalassistant.helpers.typing import ConfigType

DOMAIN = "melissa"
DATA_MELISSA = "MELISSA"


CONFIG_SCHEMA = probatio.Schema(
    {
        DOMAIN: probatio.Schema(
            {
                probatio.Required(CONF_USERNAME): cv.string,
                probatio.Required(probatio.Secret(CONF_PASSWORD)): cv.string,
            }
        )
    },
    extra=probatio.ALLOW_EXTRA,
)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the Melissa Climate component."""
    conf = config[DOMAIN]
    username = conf.get(CONF_USERNAME)
    password = conf.get(CONF_PASSWORD)
    api = AsyncMelissa(username=username, password=password)
    await api.async_connect()
    hass.data[DATA_MELISSA] = api

    hass.async_create_task(
        async_load_platform(hass, Platform.CLIMATE, DOMAIN, {}, config)
    )
    return True
