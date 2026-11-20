"""Tests for miele climate module."""

from unittest.mock import MagicMock, Mock

from aiohttp import ClientResponseError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.climate import (
    DOMAIN as CLIMATE_DOMAIN,
    ClimateService,
    ClimateServiceArgument,
)
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

pytestmark = pytest.mark.parametrize("platforms", [(Platform.CLIMATE,)])

ENTITY_ID = "climate.freezer"


@pytest.mark.parametrize("load_action_file", ["action_freezer.json"], ids=["freezer"])
async def test_climate_states(
    hass: UniversalAssistant,
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
    hass: UniversalAssistant,
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
    hass: UniversalAssistant,
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
    hass: UniversalAssistant,
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
    hass: UniversalAssistant,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
) -> None:
    """Test the climate can be turned on/off."""

    await hass.services.async_call(
        CLIMATE_DOMAIN,
        ClimateService.SET_TEMPERATURE,
        {TargetKey.ENTITY_ID: ENTITY_ID, ClimateServiceArgument.TEMPERATURE: -17},
        blocking=True,
    )
    mock_miele_client.set_target_temperature.assert_called_once_with(
        "Dummy_Appliance_1", -17.0, 1
    )


@pytest.mark.parametrize("load_action_file", ["action_freezer.json"], ids=["freezer"])
async def test_api_failure(
    hass: UniversalAssistant,
    mock_miele_client: MagicMock,
    setup_platform: MockConfigEntry,
) -> None:
    """Test handling of exception from API."""
    mock_miele_client.set_target_temperature.side_effect = ClientResponseError(
        Mock(), Mock()
    )

    with pytest.raises(
        UniversalAssistantError, match=f"Failed to set state for {ENTITY_ID}"
    ):
        await hass.services.async_call(
            CLIMATE_DOMAIN,
            ClimateService.SET_TEMPERATURE,
            {TargetKey.ENTITY_ID: ENTITY_ID, ClimateServiceArgument.TEMPERATURE: -17},
            blocking=True,
        )
    mock_miele_client.set_target_temperature.assert_called_once()
