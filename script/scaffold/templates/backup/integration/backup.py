"""Backup platform for the NEW_NAME integration."""

from universalassistant.core import __HAC_KEEP__


async def async_pre_backup(hass: __HAC_KEEP__) -> None:
    """Perform operations before a backup starts."""


async def async_post_backup(hass: __HAC_KEEP__) -> None:
    """Perform operations after a backup finishes."""
