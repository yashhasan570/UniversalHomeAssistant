"""Test the laundrify init file."""

from laundrify_aio import exceptions
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.laundrify.const import DOMAIN
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_ACCESS_TOKEN
from universalassistant.core import UniversalAssistant

from .const import VALID_ACCESS_TOKEN


async def test_setup_entry_api_unauthorized(
    hass: UniversalAssistant,
    laundrify_api_mock,
    laundrify_config_entry: MockConfigEntry,
) -> None:
    """Test that ConfigEntryAuthFailed is thrown when authentication fails."""
    laundrify_api_mock.validate_token.side_effect = exceptions.UnauthorizedException
    await hass.config_entries.async_reload(laundrify_config_entry.entry_id)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert laundrify_config_entry.state is ConfigEntryState.SETUP_ERROR
    assert not hass.data.get(DOMAIN)


async def test_setup_entry_api_cannot_connect(
    hass: UniversalAssistant,
    laundrify_api_mock,
    laundrify_config_entry: MockConfigEntry,
) -> None:
    """Test that ApiConnectionException is thrown when connection fails."""
    laundrify_api_mock.validate_token.side_effect = exceptions.ApiConnectionException
    await hass.config_entries.async_reload(laundrify_config_entry.entry_id)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert laundrify_config_entry.state is ConfigEntryState.SETUP_RETRY
    assert not hass.data.get(DOMAIN)


async def test_setup_entry_successful(
    hass: UniversalAssistant, laundrify_config_entry: MockConfigEntry
) -> None:
    """Test entry can be setup successfully."""
    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert laundrify_config_entry.state is ConfigEntryState.LOADED


async def test_setup_entry_unload(
    hass: UniversalAssistant, laundrify_config_entry: MockConfigEntry
) -> None:
    """Test unloading the laundrify entry."""
    await hass.config_entries.async_unload(laundrify_config_entry.entry_id)

    assert len(hass.config_entries.async_entries(DOMAIN)) == 1
    assert laundrify_config_entry.state is ConfigEntryState.NOT_LOADED


async def test_migrate_entry_minor_version_1_2(hass: UniversalAssistant) -> None:
    """Test migrating a 1.1 config entry to 1.2."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_ACCESS_TOKEN: VALID_ACCESS_TOKEN},
        version=1,
        minor_version=1,
        unique_id=123456,
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    assert entry.version == 1
    assert entry.minor_version == 2
    assert entry.unique_id == "123456"
