"""Test the Discord integration setup."""

from unittest.mock import patch

import nextcord

from universalassistant.components.discord.const import (
    CONF_TARGET_ID,
    DOMAIN,
    SUBENTRY_TYPE_TARGET,
)
from universalassistant.config_entries import ConfigEntryState, ConfigSubentry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import device_registry as dr, entity_registry as er

from . import (
    TARGET_NAME,
    create_entry,
    mock_exception,
    patch_discord_login,
    setup_integration,
)
from .conftest import TARGET


async def test_setup_and_unload(hass: UniversalAssistant) -> None:
    """Test the config entry sets up and unloads."""
    entry = create_entry(hass, with_subentry=True)
    await setup_integration(hass, entry)

    assert entry.state is ConfigEntryState.LOADED

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_add_subentry_reloads(
    hass: UniversalAssistant, entity_registry: er.EntityRegistry
) -> None:
    """Test adding a subentry reloads the entry so a new entity appears."""
    entry = create_entry(hass, with_subentry=True)
    await setup_integration(hass, entry)

    assert len(entity_registry.entities) == 1

    with (
        patch("universalassistant.components.discord.nextcord.Client.login"),
        patch("universalassistant.components.discord.nextcord.Client.close"),
    ):
        hass.config_entries.async_add_subentry(
            entry,
            ConfigSubentry(
                unique_id="9876543210",
                data={CONF_TARGET_ID: "9876543210"},
                subentry_type=SUBENTRY_TYPE_TARGET,
                title="alerts",
            ),
        )
        await hass.async_block_till_done()

    assert len(entity_registry.entities) == 2
    assert entity_registry.async_get("notify.alerts") is not None


async def test_setup_auth_failed(hass: UniversalAssistant) -> None:
    """Test the config entry fails to authenticate."""
    entry = create_entry(hass)
    with patch_discord_login() as mock:
        mock.side_effect = nextcord.LoginFailure
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_ERROR


async def test_setup_cannot_connect(hass: UniversalAssistant) -> None:
    """Test the config entry retries when it cannot connect."""
    entry = create_entry(hass)
    with patch_discord_login() as mock:
        mock.side_effect = mock_exception()
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_notify_entity_created(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    device_registry: dr.DeviceRegistry,
) -> None:
    """Test a notify entity and its devices are created for a target subentry."""
    entry = create_entry(hass, with_subentry=True)
    await setup_integration(hass, entry)

    subentry_id = next(iter(entry.subentries))

    entity_entry = entity_registry.async_get(f"notify.{TARGET_NAME}")
    assert entity_entry is not None
    assert entity_entry.unique_id == f"{entry.entry_id}_{TARGET}"
    assert entity_entry.config_subentry_id == subentry_id

    bot_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, entry.entry_id), entry.entry_id
    )
    assert bot_device is not None

    target_device = device_registry.async_get_device_by_identifier(
        (DOMAIN, f"{entry.entry_id}_{TARGET}"), entry.entry_id
    )
    assert target_device is not None
    assert target_device.via_device_id == bot_device.id
