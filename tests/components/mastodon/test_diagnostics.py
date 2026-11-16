"""Test Mastodon diagnostics."""

from unittest.mock import AsyncMock

from mastodon.Mastodon import MastodonNotFoundError
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_entry_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_mastodon_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test config entry diagnostics."""
    await setup_integration(hass, mock_config_entry)
    assert (
        await get_diagnostics_for_config_entry(hass, hass_client, mock_config_entry)
        == snapshot
    )


async def test_entry_diagnostics_fallback_to_instance_v1(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    mock_mastodon_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics fallback to instance_v1 when instance_v2 raises error."""
    mock_mastodon_client.instance_v2.side_effect = MastodonNotFoundError(
        "Instance v2 not found"
    )

    await setup_integration(hass, mock_config_entry)

    diagnostics_result = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )

    mock_mastodon_client.instance_v1.assert_called()

    assert diagnostics_result == snapshot
