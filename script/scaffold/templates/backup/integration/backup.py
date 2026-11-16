"""Backup platform for the NEW_NAME integration."""

from universalassistant.core import UniversalAssistant


async def async_pre_backup(hass: UniversalAssistant) -> None:
    """Perform operations before a backup starts."""


async def async_post_backup(hass: UniversalAssistant) -> None:
    """Perform operations after a backup finishes."""
