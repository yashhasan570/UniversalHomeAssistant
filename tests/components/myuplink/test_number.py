"""Tests for myuplink switch module."""

from unittest.mock import MagicMock

from aiohttp import ClientError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import DOMAIN as NUMBER_DOMAIN, NumberService
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.parametrize("platforms", [(Platform.NUMBER,)])

ENTITY_ID = "number.gotham_city_heating_offset_climate_system_1"
ENTITY_FRIENDLY_NAME = "Gotham City Heating offset climate system 1"
ENTITY_UID = "robin-r-1234-20240201-123456-aa-bb-cc-dd-ee-ff-47011"


async def test_entity_registry(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    mock_myuplink_client: MagicMock,
    setup_platform: None,
) -> None:
    """Test that the entities are registered in the entity registry."""

    entry = entity_registry.async_get(ENTITY_ID)
    assert entry.unique_id == ENTITY_UID


async def test_set_value(
    hass: __HAC_KEEP__,
    mock_myuplink_client: MagicMock,
    setup_platform: None,
) -> None:
    """Test the value of the number entity can be set."""

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {CommonServiceArgument.ENTITY_ID: ENTITY_ID, "value": 1},
        blocking=True,
    )
    await hass.async_block_till_done()
    mock_myuplink_client.async_set_device_points.assert_called_once()


async def test_api_failure(
    hass: __HAC_KEEP__,
    mock_myuplink_client: MagicMock,
    setup_platform: None,
) -> None:
    """Test handling of exception from API."""

    mock_myuplink_client.async_set_device_points.side_effect = ClientError
    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {CommonServiceArgument.ENTITY_ID: ENTITY_ID, "value": 1},
            blocking=True,
        )
    mock_myuplink_client.async_set_device_points.assert_called_once()


@pytest.mark.parametrize(
    "load_device_points_file",
    ["device_points_nibe_smo20.json"],
)
async def test_entity_registry_smo20(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    mock_myuplink_client: MagicMock,
    setup_platform: None,
) -> None:
    """Test that the entities are registered in the entity registry."""

    entry = entity_registry.async_get("number.gotham_city_change_in_curve")
    assert entry.unique_id == "robin-r-1234-20240201-123456-aa-bb-cc-dd-ee-ff-47028"


async def test_number_states(
    hass: __HAC_KEEP__,
    mock_myuplink_client: MagicMock,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: None,
) -> None:
    """Test number entity state."""

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)
