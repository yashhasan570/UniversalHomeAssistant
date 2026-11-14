"""Provide a mock package component."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.typing import ConfigType

from .const import TEST  # noqa: F401


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True
