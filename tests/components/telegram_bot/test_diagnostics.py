"""Tests for Telegram bot diagnostics."""

from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.telegram_bot.const import DOMAIN
from universalassistant.core import UniversalAssistant


async def test_diagnostics(
    hass: UniversalAssistant,
    hass_client: ClientSessionGenerator,
    webhook_bot,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics."""

    config_entry = hass.config_entries.async_entries(DOMAIN)[0]

    diagnostics = await get_diagnostics_for_config_entry(
        hass, hass_client, config_entry
    )
    assert diagnostics == snapshot
