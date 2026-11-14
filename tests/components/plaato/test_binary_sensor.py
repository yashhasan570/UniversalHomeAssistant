"""Tests for the plaato binary sensors."""

from pyplaato.models.device import PlaatoDeviceType
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.fixture
def platform() -> Platform:
    """Fixture to specify platform."""
    return Platform.BINARY_SENSOR


# note: PlaatoDeviceType.Airlock does not provide binary sensors
@pytest.mark.parametrize("device_type", [PlaatoDeviceType.Keg])
@pytest.mark.freeze_time("2024-05-24 12:00:00", tz_offset=0)
async def test_binary_sensors(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test binary sensors."""
    await snapshot_platform(hass, entity_registry, snapshot, init_integration.entry_id)
