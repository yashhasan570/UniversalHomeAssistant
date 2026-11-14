"""Test Litter-Robot diagnostics."""

from unittest.mock import MagicMock

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import __HAC_KEEP__

from .conftest import setup_integration


async def test_diagnostics(
    hass: __HAC_KEEP__,
    mock_account: MagicMock,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test generating diagnostics for a config entry."""
    entry = await setup_integration(hass, mock_account)
    diag = await get_diagnostics_for_config_entry(hass, hass_client, entry)
    assert diag == snapshot
