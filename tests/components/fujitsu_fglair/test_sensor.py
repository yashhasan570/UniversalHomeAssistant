"""Test for the sensor platform entity of the fujitsu_fglair component."""

from collections.abc import Awaitable, Callable
from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.fixture
def platforms() -> list[str]:
    """Fixture to specify platforms to test."""
    return [Platform.SENSOR]


async def test_entities(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_ayla_api: AsyncMock,
    mock_config_entry: MockConfigEntry,
    integration_setup: Callable[[], Awaitable[bool]],
) -> None:
    """Test that coordinator returns the data we expect after the first refresh."""
    assert await integration_setup()

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_no_outside_temperature(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_ayla_api: AsyncMock,
    integration_setup: Callable[[], Awaitable[bool]],
) -> None:
    """Test that the outside sensor doesn't get added if the reading is None."""
    mock_ayla_api.async_get_devices.return_value[0].outdoor_temperature = None

    assert await integration_setup()

    assert (
        len(entity_registry.entities)
        == len(mock_ayla_api.async_get_devices.return_value) - 1
    )
