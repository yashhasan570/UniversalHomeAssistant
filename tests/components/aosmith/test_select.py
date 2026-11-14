"""Tests for the select platform of the A. O. Smith integration."""

from collections.abc import AsyncGenerator
from unittest.mock import MagicMock, patch

from py_aosmith.models import OperationMode
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


@pytest.fixture(autouse=True)
async def platforms() -> AsyncGenerator[None]:
    """Return the platforms to be loaded for this test."""
    with patch("universalassistant.components.aosmith.PLATFORMS", [Platform.SELECT]):
        yield


@pytest.mark.parametrize(
    ("get_devices_fixture_supports_hot_water_plus"),
    [True],
)
async def test_state(
    hass: __HAC_KEEP__,
    init_integration: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test the state of the select entity."""
    await snapshot_platform(hass, entity_registry, snapshot, init_integration.entry_id)


@pytest.mark.parametrize(
    ("get_devices_fixture_supports_hot_water_plus"),
    [True],
)
@pytest.mark.parametrize(
    ("hass_level", "aosmith_level"),
    [
        ("off", 0),
        ("level1", 1),
        ("level2", 2),
        ("level3", 3),
    ],
)
async def test_set_hot_water_plus_level(
    hass: __HAC_KEEP__,
    mock_client: MagicMock,
    init_integration: MockConfigEntry,
    hass_level: str,
    aosmith_level: int,
) -> None:
    """Test setting the Hot Water+ level."""
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: "select.basement_my_water_heater_hot_water_plus_level",
            SelectServiceArgument.OPTION: hass_level,
        },
    )
    await hass.async_block_till_done()

    mock_client.update_mode.assert_called_once_with(
        junction_id="junctionId",
        mode=OperationMode.HEAT_PUMP,
        hot_water_plus_level=aosmith_level,
    )
