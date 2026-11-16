"""Tests for the NRGkick binary sensor platform."""

from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import STATE_OFF, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration

pytestmark = pytest.mark.usefixtures("entity_registry_enabled_by_default")


async def test_binary_sensor_entities(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nrgkick_api: AsyncMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test binary sensor entities."""
    await setup_integration(hass, mock_config_entry, platforms=[Platform.BINARY_SENSOR])

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_charge_permitted_off(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nrgkick_api: AsyncMock,
) -> None:
    """Test charge permitted binary sensor when charging is not permitted."""
    mock_nrgkick_api.get_values.return_value["general"]["charge_permitted"] = 0

    await setup_integration(hass, mock_config_entry, platforms=[Platform.BINARY_SENSOR])

    assert (state := hass.states.get("binary_sensor.nrgkick_test_charge_permitted"))
    assert state.state == STATE_OFF
