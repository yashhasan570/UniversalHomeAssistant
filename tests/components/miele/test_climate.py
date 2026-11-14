"""Tests for miele climate module."""

from unittest.mock import MagicMock, Mock

from aiohttp import ClientResponseError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.climate import DOMAIN as CLIMATE_DOMAIN
from universalassistant.const import ATTR_ENTITY_ID, ATTR_TEMPERATURE, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.parametrize("platforms", [(Platform.CLIMATE,)])

ENTITY_ID = "climate.freezer"
SERVICE_SET_TEMPERATURE = "set_temperature"


@pytest.mark.parametrize("load_action_file", ["action_freezer.json"], ids=["freezer"])
async def test_climate_states(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
) -> None:
    """Test climate entity state."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.parametrize("load_device_file", ["fridge_freezer.json"])
@pytest.mark.parametrize(
    "load_action_file", ["action_offline.json"], ids=["fridge_freezer_offline"]
)
async def test_climate_states_offline(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
) -> None:
    """Test climate entity state."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.parametrize("load_device_file", ["fridge_freezer.json"])
@pytest.mark.parametrize(
    "load_action_file", ["action_fridge_freezer.json"], ids=["fridge_freezer"]
)
async def test_climate_states_mulizone(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
) -> None:
    """Test climate entity state."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize("load_action_file", ["action_freezer.json"], ids=["freezer"])
async def test_climate_states_api_push(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    setup_platform: MockConfigEntry,
    push_data_and_actions: None,
) -> None:
    """Test climate state when the API pushes data via SSE."""

    await snapshot_platform(hass, entity_registry, snapshot, setup_platform.entry_id)


@pytest.mark.parametrize("load_action_file", ["action_freezer.json"], ids=["freezer"])
async def test_set_target(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
) -> None:
    """Test the climate can be turned on/off."""

    await hass.services.async_call(
        CLIMATE_DOMAIN,
        SERVICE_SET_TEMPERATURE,
        {ATTR_ENTITY_ID: ENTITY_ID, ATTR_TEMPERATURE: -17},
        blocking=True,
    )
    mock_miele_client.set_target_temperature.assert_called_once_with(
        "Dummy_Appliance_1", -17.0, 1
    )


@pytest.mark.parametrize("load_action_file", ["action_freezer.json"], ids=["freezer"])
async def test_api_failure(
    hass: __HAC_KEEP__,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
) -> None:
    """Test handling of exception from API."""
    mock_miele_client.set_target_temperature.side_effect = ClientResponseError(
        Mock(), Mock()
    )

    with pytest.raises(
        __HAC_KEEP__Error, match=f"Failed to set state for {ENTITY_ID}"
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            SERVICE_SET_TEMPERATURE,
            {ATTR_ENTITY_ID: ENTITY_ID, ATTR_TEMPERATURE: -17},
            blocking=True,
        )
    mock_miele_client.set_target_temperature.assert_called_once()
