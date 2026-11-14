"""Test the NEW_NAME backup platform."""

from universalassistant.components.NEW_DOMAIN.backup import (
    async_post_backup,
    async_pre_backup,
)
from universalassistant.core import UniversalAssistant


async def test_async_post_backup(hass: UniversalAssistant) -> None:
    """Verify async_post_backup."""
    # TODO: verify that the async_post_backup function executes as expected
    assert await async_post_backup(hass)


async def test_async_pre_backup(hass: UniversalAssistant) -> None:
    """Verify async_pre_backup."""
    # TODO: verify that the async_pre_backup function executes as expected
    assert await async_pre_backup(hass)
