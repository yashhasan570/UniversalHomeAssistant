"""Expose regular shell commands as services."""

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.typing import ConfigType

from .const import CONFIG_SCHEMA, DOMAIN  # noqa: F401
from .services import async_register_shell_commands, async_setup_services


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up the shell_command component."""
    async_register_shell_commands(hass, config.get(DOMAIN, {}))
    async_setup_services(hass)
    return True
