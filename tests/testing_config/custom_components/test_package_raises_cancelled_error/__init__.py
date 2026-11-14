"""Provide a mock package component."""

import asyncio

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.typing import ConfigType


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Mock a successful setup."""
    asyncio.current_task().cancel()
    await asyncio.sleep(0)
