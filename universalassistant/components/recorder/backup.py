"""Backup platform for the Recorder integration."""

from logging import getLogger

from universalassistant.core import CoreState, __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.recorder import get_instance

from .util import async_migration_in_progress

_LOGGER = getLogger(__name__)


async def async_pre_backup(hass: __HAC_KEEP__) -> None:
    """Perform operations before a backup starts."""
    _LOGGER.info("Backup start notification, locking database for writes")
    instance = get_instance(hass)
    if hass.state is not CoreState.running:
        raise __HAC_KEEP__Error("__HA_KEEP__ is not running")
    if async_migration_in_progress(hass):
        raise __HAC_KEEP__Error("Database migration in progress")
    await instance.lock_database()


async def async_post_backup(hass: __HAC_KEEP__) -> None:
    """Perform operations after a backup finishes."""
    instance = get_instance(hass)
    _LOGGER.info("Backup end notification, releasing write lock")
    if not instance.unlock_database():
        raise __HAC_KEEP__Error("Could not release database write lock")
