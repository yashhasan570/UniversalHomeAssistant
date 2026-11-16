"""Provide a mock package component."""

import asyncio

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.typing import ConfigType


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Mock a successful setup."""
    return True


async def async_setup_entry(hass: UniversalAssistant, entry: ConfigEntry) -> None:
    """Mock an leaked cancellation, without our own task being cancelled."""
    raise asyncio.CancelledError
