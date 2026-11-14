"""Tests for the BLUETTI Modbus config-entry setup."""

from unittest.mock import patch

from bluetti_modbus_lib import get_device
from freezegun.api import FrozenDateTimeFactory
from modbus_connection import (
    AcknowledgeError,
    ModbusConnectionError,
    ModbusTimeoutError,
)
from modbus_connection.mock import MockModbusUnit
import pytest
from pytest_universalassistant.common import MockConfigEntry, async_fire_time_changed

from universalassistant.components.bluetti_modbus.const import DOMAIN, SCAN_INTERVAL
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import STATE_UNAVAILABLE
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import device_registry as dr

from . import setup_integration
from .conftest import HOST, SERIAL, SERIAL_ADDRESS

VOLTAGE_ENTITY = "sensor.balco_260_battery_voltage"


async def test_load_unload_entry(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """The entry loads, produces entities, and unloads cleanly."""
    await setup_integration(hass, mock_config_entry)
    assert mock_config_entry.state is ConfigEntryState.LOADED

    state = hass.states.get(VOLTAGE_ENTITY)
    assert state is not None
    assert state.state != STATE_UNAVAILABLE

    await hass.config_entries.async_unload(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    assert mock_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_device_info(
    hass: __HAC_KEEP__,
    device_registry: dr.DeviceRegistry,
    mock_config_entry: MockConfigEntry,
) -> None:
    """The device carries its identity, firmware and a link to its web page."""
    await setup_integration(hass, mock_config_entry)

    device_entry = device_registry.async_get_device_by_identifier(
        (DOMAIN, SERIAL), mock_config_entry.entry_id
    )
    assert device_entry is not None
    assert device_entry.manufacturer == "BLUETTI"
    assert device_entry.model == "Balco 260"
    assert device_entry.model_id == "Balco260"
    assert device_entry.name == "Balco 260"
    assert device_entry.configuration_url == f"http://{HOST}"
    assert device_entry.serial_number == SERIAL
    assert device_entry.sw_version == (
        "ARM 50011.01.12, DSP 50014.01.10, IoT 50012.01.19"
    )


async def test_setup_retry_when_device_unresponsive(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
) -> None:
    """A device that answers nothing puts the entry in setup retry."""
    mock_modbus_unit.fail_requests(ModbusTimeoutError("timed out"))

    await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_setup_error_when_link_settings_are_in_use(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Another integration holding the device on other link settings is fatal."""
    with patch(
        "universalassistant.components.bluetti_modbus.async_get_unit",
        side_effect=__HAC_KEEP__Error("already in use with different link settings"),
    ):
        await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_ERROR


async def _tick(hass: __HAC_KEEP__, freezer: FrozenDateTimeFactory) -> None:
    freezer.tick(SCAN_INTERVAL)
    async_fire_time_changed(hass)
    await hass.async_block_till_done(wait_background_tasks=True)


@pytest.mark.parametrize(
    ("request_error", "teardown_error"),
    [
        pytest.param(ModbusTimeoutError("link died"), None, id="dead_link"),
        pytest.param(AcknowledgeError(), None, id="still_busy"),
        pytest.param(
            ModbusTimeoutError("link died"),
            ModbusConnectionError("teardown failed"),
            id="teardown_fails",
        ),
    ],
)
async def test_failed_refresh_goes_unavailable_then_recovers(
    hass: __HAC_KEEP__,
    freezer: FrozenDateTimeFactory,
    caplog: pytest.LogCaptureFixture,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
    request_error: Exception,
    teardown_error: Exception | None,
) -> None:
    """A device that can't be read goes unavailable, then recovers."""
    await setup_integration(hass, mock_config_entry)

    mock_modbus_unit.fail_requests(request_error)
    with patch.object(mock_modbus_unit, "disconnect", side_effect=teardown_error):
        await _tick(hass, freezer)

    state = hass.states.get(VOLTAGE_ENTITY)
    assert state is not None
    assert state.state == STATE_UNAVAILABLE
    # Reported as a failed update, not as an unexpected error with a traceback.
    assert "An error occurred while communicating with the BLUETTI" in caplog.text
    assert "Unexpected error" not in caplog.text

    mock_modbus_unit.fail_requests(None)
    await _tick(hass, freezer)

    state = hass.states.get(VOLTAGE_ENTITY)
    assert state is not None
    assert state.state != STATE_UNAVAILABLE


async def test_transient_busy_response_is_retried(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
) -> None:
    """A device that asks for a retry once does not fail the refresh."""
    read_holding_registers = mock_modbus_unit.read_holding_registers
    attempts = 0

    async def busy_once(address: int, count: int) -> list[int]:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise AcknowledgeError
        return await read_holding_registers(address, count)

    with patch.object(mock_modbus_unit, "read_holding_registers", busy_once):
        await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.LOADED

    state = hass.states.get(VOLTAGE_ENTITY)
    assert state is not None
    assert state.state != STATE_UNAVAILABLE


async def test_dead_link_on_the_retry_still_fails_the_refresh(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
) -> None:
    """A device that goes fully silent right after asking for a retry still fails."""
    attempts = 0

    async def busy_then_dead(address: int, count: int) -> list[int]:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise AcknowledgeError
        raise ModbusTimeoutError("link died")

    with patch.object(mock_modbus_unit, "read_holding_registers", busy_then_dead):
        await setup_integration(hass, mock_config_entry)

    assert mock_config_entry.state is ConfigEntryState.SETUP_RETRY


async def test_identity_mismatch_goes_unavailable_until_resolved(
    hass: __HAC_KEEP__,
    freezer: FrozenDateTimeFactory,
    caplog: pytest.LogCaptureFixture,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
) -> None:
    """A different device at the address leaves the entities unavailable."""
    await setup_integration(hass, mock_config_entry)

    mock_modbus_unit.holding[SERIAL_ADDRESS] = 1
    await _tick(hass, freezer)

    state = hass.states.get(VOLTAGE_ENTITY)
    assert state is not None
    assert state.state == STATE_UNAVAILABLE
    assert "is a different device than the one this entry" in caplog.text

    mock_modbus_unit.holding[SERIAL_ADDRESS] = int(SERIAL)
    await _tick(hass, freezer)

    state = hass.states.get(VOLTAGE_ENTITY)
    assert state is not None
    assert state.state != STATE_UNAVAILABLE


async def test_excluded_fields_are_dropped_from_the_read_plan(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_modbus_unit: MockModbusUnit,
) -> None:
    """A field with no entity yet is not polled either, not just not created."""
    await setup_integration(hass, mock_config_entry)

    ac_output = get_device("balco260").get_field("ac_o_switch")
    assert ac_output is not None
    assert mock_modbus_unit.read_events
    assert not any(
        event.address <= ac_output.address < event.address + event.count
        for event in mock_modbus_unit.read_events
    )
