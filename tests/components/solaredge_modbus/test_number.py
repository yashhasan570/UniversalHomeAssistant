"""Tests for the SolarEdge Modbus number entities."""

from unittest.mock import patch

from modbus_connection import ModbusTimeoutError
from modbus_connection.mock import MockModbusUnit
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

BACKUP_RESERVE_ENTITY = "number.solaredge_se10000h_backup_reserve"
BACKUP_RESERVE_REGISTER = 57352


async def _setup_number_platform(hass: UniversalAssistant, entry: MockConfigEntry) -> None:
    with patch(
        "universalassistant.components.solaredge_modbus.PLATFORMS", [Platform.NUMBER]
    ):
        entry.add_to_hass(hass)
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_numbers(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """All number entities and their states match the snapshot."""
    await _setup_number_platform(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_power_factor_setpoint_disabled_by_default(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Reactive power is grid-code territory and stays out of the way."""
    await _setup_number_platform(hass, mock_config_entry)

    entity_id = "number.solaredge_se10000h_power_factor_setpoint"

    assert hass.states.get(entity_id) is None
    entry = entity_registry.async_get(entity_id)
    assert entry is not None
    assert entry.disabled_by is er.RegistryEntryDisabler.INTEGRATION


async def test_set_value(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
) -> None:
    """Setting a number writes to the device and updates the state."""
    await _setup_number_platform(hass, mock_config_entry)

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {
            CommonServiceArgument.ENTITY_ID: BACKUP_RESERVE_ENTITY,
            NumberServiceArgument.VALUE: 25,
        },
        blocking=True,
    )
    await hass.async_block_till_done()

    state = hass.states.get(BACKUP_RESERVE_ENTITY)
    assert state is not None
    assert state.state == "25.0"


async def test_set_value_communication_error(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
) -> None:
    """A write that fails on the wire raises a translated error."""
    await _setup_number_platform(hass, mock_config_entry)

    mock_modbus_unit.fail_write(BACKUP_RESERVE_REGISTER, ModbusTimeoutError("timeout"))

    with pytest.raises(UniversalAssistantError) as excinfo:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: BACKUP_RESERVE_ENTITY,
                NumberServiceArgument.VALUE: 25,
            },
            blocking=True,
        )

    assert excinfo.value.translation_key == "communication_error"


async def test_set_value_rejected(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
) -> None:
    """A value the device rejects raises a translated error."""
    await _setup_number_platform(hass, mock_config_entry)

    mock_modbus_unit.fail_write(BACKUP_RESERVE_REGISTER, ValueError("does not fit"))

    with pytest.raises(UniversalAssistantError) as excinfo:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: BACKUP_RESERVE_ENTITY,
                NumberServiceArgument.VALUE: 25,
            },
            blocking=True,
        )

    assert excinfo.value.translation_key == "rejected_value"
