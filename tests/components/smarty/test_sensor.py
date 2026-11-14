"""Tests for the Smarty sensor platform."""

from datetime import timedelta
from unittest.mock import AsyncMock, patch

from freezegun.api import FrozenDateTimeFactory
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    async_fire_time_changed,
    snapshot_platform,
)
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration


@pytest.mark.freeze_time("2023-10-21")
async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_smarty: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.smarty.PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_retry_after_failure(
    hass: __HAC_KEEP__,
    mock_smarty: AsyncMock,
    mock_config_entry: MockConfigEntry,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test retrying once after a transient update failure."""
    with patch("universalassistant.components.smarty.PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)

    mock_smarty.update.reset_mock()
    mock_smarty.update.side_effect = [False, False, True]

    # First scheduled update fails after the normal 30-second interval.
    freezer.tick(timedelta(seconds=30))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert mock_smarty.update.call_count == 1

    # The coordinator retries after 2 seconds.
    freezer.tick(timedelta(seconds=2))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert mock_smarty.update.call_count == 2

    # A second consecutive failure falls back to the normal interval.
    freezer.tick(timedelta(seconds=2))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert mock_smarty.update.call_count == 2

    # The next update occurs after the normal 30-second interval.
    freezer.tick(timedelta(seconds=28))
    async_fire_time_changed(hass)
    await hass.async_block_till_done()

    assert mock_smarty.update.call_count == 3
