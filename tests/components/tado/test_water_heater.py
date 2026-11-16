"""The water heater tests for the tado platform."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.tado import DOMAIN
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er


@pytest.fixture(autouse=True)
def setup_platforms() -> Generator[None]:
    """Set up the platforms for the tests."""
    with patch("universalassistant.components.tado.PLATFORMS", [Platform.WATER_HEATER]):
        yield


@pytest.mark.usefixtures("init_integration")
async def test_entities(
    hass: UniversalAssistant, entity_registry: er.EntityRegistry, snapshot: SnapshotAssertion
) -> None:
    """Test creation of water heater."""

    config_entry: MockConfigEntry = hass.config_entries.async_entries(DOMAIN)[0]

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)
