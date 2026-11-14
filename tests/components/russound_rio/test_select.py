"""Tests for the Russound RIO select platform."""

from unittest.mock import AsyncMock, patch

from aiorussound.rio.models import PartyMode
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import setup_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    mock_russound_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.russound_rio.PLATFORMS", [Platform.SELECT]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_setting_value(
    hass: __HAC_KEEP__,
    mock_russound_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting value."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: "select.backyard_backyard_party_mode",
            SelectServiceArgument.OPTION: "master",
        },
        blocking=True,
    )
    mock_russound_client.controllers[1].zones[1].set_party_mode.assert_called_once_with(
        PartyMode.MASTER
    )
    mock_russound_client.controllers[1].zones[1].set_party_mode.reset_mock()
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: "select.backyard_backyard_party_mode",
            SelectServiceArgument.OPTION: "off",
        },
        blocking=True,
    )
    mock_russound_client.controllers[1].zones[1].set_party_mode.assert_called_once_with(
        PartyMode.OFF
    )
