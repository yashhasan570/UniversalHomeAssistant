"""Test SMLIGHT diagnostics."""

from unittest.mock import MagicMock

from pytest_universalassistant.common import MockConfigEntry, async_load_fixture
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.smlight.const import DOMAIN
from universalassistant.core import __HAC_KEEP__

from .conftest import setup_integration


async def test_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    mock_config_entry: MockConfigEntry,
    mock_smlight_client: MagicMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    mock_smlight_client.get.return_value = await async_load_fixture(
        hass, "logs.txt", DOMAIN
    )
    entry = await setup_integration(hass, mock_config_entry)

    result = await get_diagnostics_for_config_entry(hass, hass_client, entry)

    assert result == snapshot
