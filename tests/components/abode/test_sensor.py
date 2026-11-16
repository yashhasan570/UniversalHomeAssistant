"""Tests for the Abode sensor device."""

from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from .common import setup_platform


async def test_all_entities(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test all entities."""
    config_entry = await setup_platform(hass, SENSOR_DOMAIN)

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
