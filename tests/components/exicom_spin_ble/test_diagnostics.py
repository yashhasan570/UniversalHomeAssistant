"""Tests for the Spin EV Charger diagnostics."""

from dataclasses import replace
from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from spinev_ble import ChargerStatus
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from . import setup_integration
from .const import STATUS


@pytest.mark.parametrize(
    "status",
    [
        pytest.param(
            replace(STATUS, alarms=("Mains Low", "Earth Wire Open")), id="alarms"
        ),
        # The raw value is what identifies a state the library does not know.
        pytest.param(replace(STATUS, state=None, state_value=99), id="unrecognised"),
    ],
)
async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    mock_charger: AsyncMock,
    snapshot: SnapshotAssertion,
    status: ChargerStatus,
) -> None:
    """Diagnostics carry the last status with the address and serial redacted."""
    mock_charger.async_get_status.return_value = status
    await setup_integration(hass, mock_config_entry)

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )
