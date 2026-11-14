"""Test the Tessie device tracker platform."""

from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from .common import assert_entities, setup_platform


async def test_device_tracker(
    hass: __HAC_KEEP__, snapshot: SnapshotAssertion, entity_registry: er.EntityRegistry
) -> None:
    """Tests that the device tracker entities are correct."""

    entry = await setup_platform(hass, [Platform.DEVICE_TRACKER])

    assert_entities(hass, entry.entry_id, entity_registry, snapshot)
