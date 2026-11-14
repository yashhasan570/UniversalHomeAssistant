"""Tests for the diagnostics data provided by the Roku integration."""

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from rokuecp import Device as RokuDevice
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import __HAC_KEEP__
from universalassistant.util import dt as dt_util


async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    mock_device: RokuDevice,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for config entry."""
    mock_device.state.at = dt_util.parse_datetime("2023-08-15 17:00:00-00:00")

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, init_integration)
        == snapshot
    )
