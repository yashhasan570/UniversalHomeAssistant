"""Test the Nina diagnostics."""

from unittest.mock import AsyncMock

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from . import setup_platform


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    mock_nina_class: AsyncMock,
    nina_warnings: list[Warning],
) -> None:
    """Test diagnostics."""

    await setup_platform(hass, mock_config_entry, mock_nina_class, nina_warnings)
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )
