"""Test EcoNet binary sensors."""

from collections.abc import Awaitable, Callable

from pyeconet.equipment import Equipment
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.const import STATE_ON, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.parametrize("platform", [Platform.BINARY_SENSOR])


@pytest.mark.parametrize(
    "equipment_data", ["water_heater", "thermostat"], indirect=True
)
async def test_binary_sensors(
    hass: UniversalAssistant,
    setup_integration: Callable[[], Awaitable[None]],
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Binary sensors have translated names, stable unique IDs, and states."""
    await setup_integration()
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_running_updates(
    hass: UniversalAssistant,
    setup_integration: Callable[[], Awaitable[None]],
    mock_equipment: Equipment,
) -> None:
    """The renamed running binary sensor still receives updates."""
    await setup_integration()
    mock_equipment.update_equipment_info(
        {"device_name": "device_1", "@RUNNING": "Running"}
    )
    await hass.async_block_till_done()
    assert hass.states.get("binary_sensor.gas_water_heater_running").state == STATE_ON
