"""Velbus select platform tests."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import Platform, TargetKey
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
    with patch("universalassistant.components.velbus.PLATFORMS", [Platform.SELECT]):
        await init_integration(hass, config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, config_entry.entry_id)


@pytest.mark.parametrize(
    ("set_program"), [("none"), ("summer"), ("winter"), ("holiday")]
)
async def test_select_program(
    hass: UniversalAssistant,
    mock_select: AsyncMock,
    config_entry: MockConfigEntry,
    set_program: str,
) -> None:
    """Test program selection."""
    await init_integration(hass, config_entry)
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            TargetKey.ENTITY_ID: "select.kitchen_program",
            SelectServiceArgument.OPTION: set_program,
        },
        blocking=True,
    )
    mock_select.set_selected_program.assert_called_once_with(set_program)
