"""Test number platform for Nintendo Parental Controls."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import setup_integration


async def test_number(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nintendo_client: AsyncMock,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test number platform."""
    with patch(
        "universalassistant.components.nintendo_parental_controls._PLATFORMS",
        [Platform.NUMBER],
    ):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_set_number(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_nintendo_client: AsyncMock,
    mock_nintendo_device: AsyncMock,
) -> None:
    """Test number platform service."""
    with patch(
        "universalassistant.components.nintendo_parental_controls._PLATFORMS",
        [Platform.NUMBER],
    ):
        await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        service_data={NumberServiceArgument.VALUE: "120"},
        target={TargetKey.ENTITY_ID: "number.universal_assistant_test_max_screentime_today"},
        blocking=True,
    )
    assert len(mock_nintendo_device.update_max_daily_playtime.mock_calls) == 1
