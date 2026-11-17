"""Test the Fressnapf Tracker switch platform."""

from collections.abc import AsyncGenerator
from unittest.mock import MagicMock, patch

from fressnapftracker import (
    FressnapfTrackerError,
    FressnapfTrackerInvalidTokenError,
    Tracker,
    TrackerFeatures,
    TrackerSettings,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import (
    DOMAIN as SWITCH_DOMAIN,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    SwitchService,
)
from universalassistant.const import ATTR_ENTITY_ID, STATE_ON, Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ConfigEntryAuthFailed, UniversalAssistantError
from universalassistant.helpers import entity_registry as er

TRACKER_NO_ENERGY_SAVING_MODE = Tracker(
    name="Fluffy",
    battery=0,
    charging=False,
    position=None,
    tracker_settings=TrackerSettings(
        generation="GPS Tracker 2.0",
        features=TrackerFeatures(energy_saving_mode=False),
    ),
)


@pytest.fixture(autouse=True)
async def platforms() -> AsyncGenerator[None]:
    """Return the platforms to be loaded for this test."""
    with patch(
        "universalassistant.components.fressnapf_tracker.PLATFORMS", [Platform.SWITCH]
    ):
        yield


@pytest.mark.usefixtures("init_integration")
async def test_state_entity_device_snapshots(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test switch entity is created correctly."""
    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.usefixtures("mock_auth_client")
async def test_not_added_when_no_energy_saving_mode(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    mock_api_client_init: MagicMock,
) -> None:
    """Test switch entity is created correctly."""
    mock_api_client_init.get_tracker.return_value = TRACKER_NO_ENERGY_SAVING_MODE

    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_entries = er.async_entries_for_config_entry(
        entity_registry, mock_config_entry.entry_id
    )
    assert len(entity_entries) == 0


@pytest.mark.usefixtures("init_integration")
async def test_turn_on(
    hass: UniversalAssistant,
    mock_api_client_coordinator: MagicMock,
) -> None:
    """Test turning the switch on."""
    entity_id = "switch.fluffy_sleep_mode"

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {TargetKey.ENTITY_ID: entity_id},
        blocking=True,
    )

    mock_api_client_coordinator.set_energy_saving.assert_called_once_with(True)


@pytest.mark.usefixtures("init_integration")
async def test_turn_off(
    hass: UniversalAssistant,
    mock_api_client_coordinator: MagicMock,
) -> None:
    """Test turning the switch off."""
    entity_id = "switch.fluffy_sleep_mode"

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_ON

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {TargetKey.ENTITY_ID: entity_id},
        blocking=True,
    )

    mock_api_client_coordinator.set_energy_saving.assert_called_once_with(False)


@pytest.mark.parametrize(
    ("api_exception", "expected_exception"),
    [
        (FressnapfTrackerError("Something went wrong"), UniversalAssistantError),
        (
            FressnapfTrackerInvalidTokenError("Token no longer valid"),
            ConfigEntryAuthFailed,
        ),
    ],
)
@pytest.mark.parametrize("service", [SERVICE_TURN_ON, SERVICE_TURN_OFF])
@pytest.mark.usefixtures("mock_auth_client", "mock_api_client_init")
async def test_turn_on_off_error(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    mock_api_client_coordinator: MagicMock,
    api_exception: FressnapfTrackerError,
    expected_exception: type[UniversalAssistantError],
    service: str,
) -> None:
    """Test that errors during service handling are handled correctly."""

    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = "switch.fluffy_sleep_mode"

    mock_api_client_coordinator.set_energy_saving.side_effect = api_exception
    with pytest.raises(expected_exception):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            service,
            {ATTR_ENTITY_ID: entity_id},
            blocking=True,
        )
