"""Provide a mock package component."""

import asyncio

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.typing import ConfigType


async def async_setup(hass: __HAC_KEEP__, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True


async def async_setup_entry(hass: __HAC_KEEP__, entry: ConfigEntry) -> None:
    """Mock an leaked cancellation, without our own task being cancelled."""
    raise asyncio.CancelledError
