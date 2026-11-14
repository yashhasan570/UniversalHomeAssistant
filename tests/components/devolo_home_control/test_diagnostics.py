"""Tests for the devolo Home Control diagnostics."""

from unittest.mock import patch

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import __HAC_KEEP__

from . import configure_integration
from .mocks import HomeControlMock, HomeControlMockBinarySensor


async def test_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test setup and state change of a climate device."""
    entry = configure_integration(hass)
    gateway_1 = HomeControlMockBinarySensor()
    gateway_2 = HomeControlMock()
    with patch(
        "universalassistant.components.devolo_home_control.HomeControl",
        side_effect=[gateway_1, gateway_2],
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

        assert entry.state is ConfigEntryState.LOADED

        result = await get_diagnostics_for_config_entry(hass, hass_client, entry)
        assert result == snapshot(exclude=props("created_at", "modified_at"))
