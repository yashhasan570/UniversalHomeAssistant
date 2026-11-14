"""Tests for the Discord integration."""

from unittest.mock import AsyncMock, Mock, patch

import nextcord
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.discord.const import (
    CONF_TARGET_ID,
    DOMAIN,
    SUBENTRY_TYPE_TARGET,
)
from universalassistant.config_entries import ConfigSubentryData
from universalassistant.const import CONF_API_TOKEN, CONF_NAME
from universalassistant.core import UniversalAssistant

from .conftest import TARGET

TOKEN = "abc123"
NAME = "Discord Bot"
TARGET_NAME = "general"

CONF_INPUT = {CONF_API_TOKEN: TOKEN}

CONF_DATA = {
    CONF_API_TOKEN: TOKEN,
    CONF_NAME: NAME,
}


def create_entry(hass: UniversalAssistant, with_subentry: bool = False) -> MockConfigEntry:
    """Add config entry in Universal Universal Home Assistant."""
    subentries_data = None
    if with_subentry:
        subentries_data = [
            ConfigSubentryData(
                unique_id=TARGET,
                data={CONF_TARGET_ID: TARGET},
                subentry_type=SUBENTRY_TYPE_TARGET,
                title=TARGET_NAME,
            )
        ]
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=CONF_DATA,
        unique_id="1234567890",
        subentries_data=subentries_data,
    )
    entry.add_to_hass(hass)
    return entry


def mocked_discord_info():
    """Create mocked discord."""
    mocked_discord = AsyncMock()
    mocked_discord.id = "1234567890"
    mocked_discord.name = NAME
    return patch(
        "universalassistant.components.discord.config_flow.nextcord.Client.application_info",
        return_value=mocked_discord,
    )


def patch_discord_login():
    """Patch discord info."""
    return patch("universalassistant.components.discord.config_flow.nextcord.Client.login")


async def setup_integration(hass: UniversalAssistant, entry: MockConfigEntry) -> None:
    """Set up the Discord integration for the given config entry."""
    with (
        patch("universalassistant.components.discord.nextcord.Client.login"),
        patch("universalassistant.components.discord.nextcord.Client.close"),
    ):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()


def mock_exception():
    """Mock response."""
    response = Mock()
    response.status = 404
    return nextcord.HTTPException(response, "")
