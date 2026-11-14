"""Test the sensor classes for youless."""

from unittest.mock import patch

from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import init_component


async def test_sensors(
    hass: __HAC_KEEP__, entity_registry: er.EntityRegistry, snapshot: SnapshotAssertion
) -> None:
    """Test the sensor classes for youless."""
    with patch("universalassistant.components.youless.PLATFORMS", [Platform.SENSOR]):
        entry = await init_component(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
