"""Tests for the sensor platform of the A. O. Smith integration."""

from collections.abc import AsyncGenerator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.fixture(autouse=True)
async def platforms() -> AsyncGenerator[None]:
    """Return the platforms to be loaded for this test."""
    with patch("universalassistant.components.aosmith.PLATFORMS", [Platform.SENSOR]):
        yield


async def test_state(
    hass: __HAC_KEEP__,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test the state of the sensor entities."""
    await snapshot_platform(hass, entity_registry, snapshot, init_integration.entry_id)
