"""Test schlage sensor."""

from collections.abc import Awaitable, Callable
from unittest.mock import patch

from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import MockSchlageConfigEntry


async def test_sensor_attributes(
    hass: __HAC_KEEP__,
    mock_add_config_entry: Callable[[], Awaitable[MockSchlageConfigEntry]],
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test sensor attributes."""
    with patch("universalassistant.components.schlage.PLATFORMS", [Platform.SENSOR]):
        config_entry = await mock_add_config_entry()
        await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
