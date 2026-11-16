"""Test the NeoPool diagnostics."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.diagnostics import REDACTED
from universalassistant.components.neopool.diagnostics import (
    async_get_config_entry_diagnostics,
)
from universalassistant.core import UniversalAssistant

from . import setup_integration


@pytest.mark.usefixtures("mock_neopool_client")
async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test config entry diagnostics output is stable and redacts host/port."""
    await setup_integration(hass, mock_config_entry)

    result = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )

    assert result == snapshot(
        exclude=props(
            "created_at",
            "modified_at",
            "entry_id",
        )
    )


@pytest.mark.usefixtures("mock_neopool_client")
async def test_entry_diagnostics_redacts_serial_device(
    hass: UniversalAssistant,
    mock_config_entry_serial: MockConfigEntry,
) -> None:
    """The serial device path is redacted; it can carry a USB adapter serial."""
    await setup_integration(hass, mock_config_entry_serial)

    result = await async_get_config_entry_diagnostics(hass, mock_config_entry_serial)

    assert result["config_entry"]["data"]["device"] == REDACTED
    assert "/dev/ttyUSB0" not in str(result)


@pytest.mark.usefixtures("mock_neopool_client")
async def test_entry_diagnostics_exposes_only_exception_type(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """last_exception exposes the type only, never the raw message.

    The client embeds host:port in connection error messages, so the raw
    text must never be serialized into diagnostics.
    """
    await setup_integration(hass, mock_config_entry)
    coordinator = mock_config_entry.runtime_data
    coordinator.last_exception = ConnectionError(
        "Modbus client connection failed to 192.0.2.15:502"
    )
    result = await async_get_config_entry_diagnostics(hass, mock_config_entry)
    assert result["coordinator"]["last_exception"] == "ConnectionError"
    assert "192.0.2.15" not in str(result)
