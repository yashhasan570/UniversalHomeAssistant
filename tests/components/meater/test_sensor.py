"""Tests for the Meater sensors."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration


@pytest.mark.freeze_time("2023-10-21")
async def test_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_meater_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the sensor entities."""
    with patch("universalassistant.components.meater.PLATFORMS", [Platform.SENSOR]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
