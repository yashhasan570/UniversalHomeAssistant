"""Provide a mock package component."""

import asyncio

from universalassistant.core import UniversalAssistant
from universalassistant.helpers.typing import ConfigType


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Mock a successful setup."""
    asyncio.current_task().cancel()
    await asyncio.sleep(0)
