"""Tests for the Qube Heat Pump select platform."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import setup_integration

ENTITY_ID = "select.qube_heat_pump_smart_grid_ready_mode"


async def test_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_qube_client: MagicMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test all select entities via snapshot."""
    with patch("universalassistant.components.hr_energy_qube.PLATFORMS", [Platform.SELECT]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize("option", ["block", "plus", "max"])
async def test_select_option(
    hass: UniversalAssistant,
    mock_qube_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    option: str,
) -> None:
    """Test selecting an SG Ready mode."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: ENTITY_ID,
            SelectServiceArgument.OPTION: option,
        },
        blocking=True,
    )

    mock_qube_client.set_sg_ready_mode.assert_awaited_once_with(option)


@pytest.mark.parametrize(
    ("side_effect", "return_value"),
    [
        (ConnectionError, None),
        (None, False),
    ],
)
async def test_select_option_error(
    hass: UniversalAssistant,
    mock_qube_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    side_effect: type[Exception] | None,
    return_value: bool | None,
) -> None:
    """Test select raises UniversalAssistantError on connection error or write failure."""
    await setup_integration(hass, mock_config_entry)

    mock_qube_client.set_sg_ready_mode = AsyncMock(
        side_effect=side_effect, return_value=return_value
    )
    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: ENTITY_ID,
                SelectServiceArgument.OPTION: "plus",
            },
            blocking=True,
        )
