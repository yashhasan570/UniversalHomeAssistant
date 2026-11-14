"""Backup platform for the Recorder integration."""

from logging import getLogger

from universalassistant.core import CoreState, UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers.recorder import get_instance

from .util import async_migration_in_progress

_LOGGER = getLogger(__name__)


async def async_pre_backup(hass: UniversalAssistant) -> None:
    """Perform operations before a backup starts."""
    _LOGGER.info("Backup start notification, locking database for writes")
    instance = get_instance(hass)
    if hass.state is not CoreState.running:
        raise UniversalAssistantError("Universal Universal Home Assistant is not running")
    if async_migration_in_progress(hass):
        raise UniversalAssistantError("Database migration in progress")
    await instance.lock_database()


async def async_post_backup(hass: UniversalAssistant) -> None:
    """Perform operations after a backup finishes."""
    instance = get_instance(hass)
    _LOGGER.info("Backup end notification, releasing write lock")
    if not instance.unlock_database():
        raise UniversalAssistantError("Could not release database write lock")
