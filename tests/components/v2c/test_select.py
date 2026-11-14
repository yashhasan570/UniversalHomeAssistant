"""Test the V2C select platform."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from pytrydan.models.trydan import ChargeMode
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import init_integration


async def test_select(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test states of the select entities."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.SELECT]):
        await init_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_select_option(
    hass: __HAC_KEEP__,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test selecting an option."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.SELECT]):
        await init_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: "select.evse_1_1_1_1_charge_mode",
            SelectServiceArgument.OPTION: "mixed",
        },
        blocking=True,
    )

    mock_v2c_client.charge_mode.assert_awaited_once_with(ChargeMode.MIXED)


async def test_select_not_created_when_missing(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test missing charge mode entity is not created."""
    mock_v2c_client.get_data.return_value.charge_mode = None

    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.SELECT]):
        await init_integration(hass, mock_config_entry)

    entity_id = "select.evse_1_1_1_1_charge_mode"
    assert entity_registry.async_get(entity_id) is None
    assert hass.states.get(entity_id) is None
