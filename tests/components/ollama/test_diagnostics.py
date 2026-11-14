"""Test Ollama diagnostics."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import __HAC_KEEP__


@pytest.mark.parametrize(
    "has_token",
    [
        pytest.param(True, id="api_key"),
        pytest.param(False, id="no_api_key"),
    ],
)
@pytest.mark.usefixtures("mock_init_component")
async def test_entry_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    mock_config_entry_with_assist: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    assert (
        await get_diagnostics_for_config_entry(
            hass, hass_client, mock_config_entry_with_assist
        )
        == snapshot
    )
