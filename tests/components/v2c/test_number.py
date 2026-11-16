"""Test the V2C number platform."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import init_integration


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_number(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test states of the number entities."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.NUMBER]):
        await init_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_number_set_value(
    hass: UniversalAssistant,
    mock_v2c_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test setting number values."""
    with patch("universalassistant.components.v2c.PLATFORMS", [Platform.NUMBER]):
        await init_integration(hass, mock_config_entry)

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {
            CommonServiceArgument.ENTITY_ID: "number.evse_1_1_1_1_installation_voltage",
            NumberServiceArgument.VALUE: 240,
        },
        blocking=True,
    )

    mock_v2c_client.voltage_installation.assert_called_once_with(240)
