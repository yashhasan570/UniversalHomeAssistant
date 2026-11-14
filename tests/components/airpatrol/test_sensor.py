"""Test the AirPatrol sensor platform."""

from collections.abc import Generator
from unittest.mock import patch

from airpatrol.api import AirPatrolAPI
import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    SnapshotAssertion,
    snapshot_platform,
)

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.fixture(autouse=True)
def override_platforms() -> Generator[None]:
    """Override the platforms to load for airpatrol."""
    with patch(
        "universalassistant.components.airpatrol.PLATFORMS",
        [Platform.SENSOR],
    ):
        yield


async def test_sensor_with_climate_data(
    hass: __HAC_KEEP__,
    load_integration: MockConfigEntry,
    get_client: AirPatrolAPI,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test sensor entities are created with climate data."""
    await snapshot_platform(
        hass,
        entity_registry,
        snapshot,
        load_integration.entry_id,
    )


@pytest.mark.parametrize(
    "climate_data",
    [
        None,
    ],
)
async def test_sensor_with_no_climate_data(
    hass: __HAC_KEEP__,
    load_integration: MockConfigEntry,
    get_client: AirPatrolAPI,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test no sensor entities are created when no climate data is present."""
    assert len(entity_registry.entities) == 0
