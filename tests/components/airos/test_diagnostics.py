"""Diagnostic tests for airOS."""

from unittest.mock import AsyncMock, MagicMock

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import Any, ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.airos.coordinator import AirOS8Data
from universalassistant.core import __HAC_KEEP__

from . import setup_integration


async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    mock_airos_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    ap_status_fixture: AirOS8Data,
    ap_firmware_fixture: dict[str, Any],
    snapshot: SnapshotAssertion,
    mock_async_get_firmware_data: AsyncMock,
) -> None:
    """Test diagnostics."""

    await setup_integration(hass, mock_config_entry)

    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )
