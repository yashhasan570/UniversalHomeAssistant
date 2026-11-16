"""Velbus cover platform tests."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.cover import (
    DOMAIN as COVER_DOMAIN,
    CoverService,
    CoverServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import entity_registry as er

from . import init_integration


async def test_entities(
    hass: UniversalAssistant,
    snapshot: SnapshotAssertion,
    config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    with patch("universalassistant.components.velbus.PLATFORMS", [Platform.COVER]):
        await init_integration(hass, config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.parametrize(
    ("entity_id", "entity_num"),
    [
        ("cover.basement_covername", 0),
        ("cover.basement_covernamenopos", 1),
    ],
)
async def test_actions(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    entity_id: str,
    entity_num: int,
) -> None:
    """Test the cover actions."""
    await init_integration(hass, config_entry)
    entity = config_entry.runtime_data.controller.get_all_cover()[entity_num]
    await hass.services.async_call(
        COVER_DOMAIN,
        CoverService.CLOSE,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    entity.close.assert_called_once()
    await hass.services.async_call(
        COVER_DOMAIN,
        CoverService.OPEN,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    entity.open.assert_called_once()
    await hass.services.async_call(
        COVER_DOMAIN,
        CoverService.STOP,
        {CommonServiceArgument.ENTITY_ID: entity_id},
        blocking=True,
    )
    entity.stop.assert_called_once()


async def test_position(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    mock_cover: AsyncMock,
) -> None:
    """Test the set_postion over action."""
    await init_integration(hass, config_entry)
    await hass.services.async_call(
        COVER_DOMAIN,
        CoverService.SET_POSITION,
        {
            CommonServiceArgument.ENTITY_ID: "cover.basement_covername",
            CoverServiceArgument.POSITION: 25,
        },
        blocking=True,
    )
    mock_cover.set_position.assert_called_once_with(75)
