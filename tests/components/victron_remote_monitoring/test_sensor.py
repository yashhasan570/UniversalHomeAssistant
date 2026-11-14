"""Tests for the VRM Forecasts sensors.

Consolidates most per-sensor assertions into snapshot-based regression tests.
"""

import pytest
from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors_snapshot(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    init_integration,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot all VRM sensor states & key attributes."""
    await snapshot_platform(hass, entity_registry, snapshot, init_integration.entry_id)
