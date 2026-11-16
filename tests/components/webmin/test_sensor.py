"""Test cases for the Webmin sensors."""

import pytest
from pytest_universalassistant.common import snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from .conftest import async_init_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensor(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the sensor entities and states."""

    entry = await async_init_integration(hass)

    await snapshot_platform(hass, entity_registry, snapshot, entry.entry_id)
