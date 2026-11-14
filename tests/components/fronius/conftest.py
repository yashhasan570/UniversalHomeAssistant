"""Fixtures for the Fronius integration tests."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

from modbus_connection import ModbusConnectionError
from modbus_connection.mock import MockModbusConnection
import pytest

from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__


@pytest.fixture(autouse=True)
def mock_modbus_unavailable(
    mock_modbus_connection: MockModbusConnection,
) -> Generator[MagicMock]:
    """Refuse every Modbus request by default so tests run HTTP-only."""

    def _refusing_unit(
        hass: __HAC_KEEP__, entry: ConfigEntry, params: object, unit_id: int
    ) -> object:
        unit = mock_modbus_connection.for_unit(unit_id)
        unit.fail_requests(ModbusConnectionError("Modbus disabled in tests"))
        return unit

    with patch(
        "universalassistant.components.fronius.modbus.async_get_unit",
        MagicMock(side_effect=_refusing_unit),
    ) as mock_get_unit:
        yield mock_get_unit


@pytest.fixture
def mock_fronius_modbus(
    mock_modbus_unavailable: MagicMock,
    mock_modbus_connection: MockModbusConnection,
) -> MockModbusConnection:
    """Answer Modbus requests from the mock connection."""
    mock_modbus_unavailable.side_effect = lambda hass, entry, params, unit_id: (
        mock_modbus_connection.for_unit(unit_id)
    )
    return mock_modbus_connection
