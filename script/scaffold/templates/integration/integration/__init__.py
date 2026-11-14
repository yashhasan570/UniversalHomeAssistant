"""The NEW_NAME integration."""

import probatio

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.typing import ConfigType

from .const import DOMAIN

CONFIG_SCHEMA = probatio.Schema(
    {probatio.Optional(DOMAIN): {}}, extra=probatio.ALLOW_EXTRA
)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the NEW_NAME integration."""
    return True
