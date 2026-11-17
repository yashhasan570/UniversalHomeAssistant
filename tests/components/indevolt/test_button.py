"""Tests for the Indevolt button platform."""

from unittest.mock import AsyncMock, patch

from indevolt_api import IndevoltConfig, IndevoltEnergyMode
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.button import DOMAIN as BUTTON_DOMAIN, ButtonService
from universalassistant.const import Platform, TargetKey
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError
from universalassistant.helpers import entity_registry as er

from . import setup_integration

ENTITY_ID_GEN2 = "button.cms_sf2000_enable_standby_mode"
ENTITY_ID_GEN1 = "button.bk1600_enable_standby_mode"


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize("generation", [2, 1], indirect=True)
async def test_button(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    mock_indevolt: AsyncMock,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test button entity registration and states."""
    with patch("universalassistant.components.indevolt.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


@pytest.mark.parametrize("generation", [2], indirect=True)
async def test_button_press_standby(
    hass: UniversalAssistant,
    mock_indevolt: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test standby button switches to real-time mode and sends action."""
    with patch("universalassistant.components.indevolt.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    # Reset mock call count for this iteration
    mock_indevolt.set_data.reset_mock()

    # Mock call to pause (dis)charging
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: ENTITY_ID_GEN2},
        blocking=True,
    )

    # Verify set_data was called for mode switch and stop() was called
    mock_indevolt.set_data.assert_called_once_with(
        IndevoltConfig.WRITE_ENERGY_MODE, IndevoltEnergyMode.REAL_TIME_CONTROL
    )
    mock_indevolt.stop.assert_called_once()


@pytest.mark.parametrize("generation", [2], indirect=True)
async def test_button_press_standby_already_in_realtime_mode(
    hass: UniversalAssistant,
    mock_indevolt: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test pressing standby when already in real-time mode skips the mode switch."""

    # Force real-time control mode
    mock_indevolt.fetch_data.return_value[IndevoltConfig.READ_ENERGY_MODE] = (
        IndevoltEnergyMode.REAL_TIME_CONTROL
    )
    with patch("universalassistant.components.indevolt.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    # Reset mock call count for this iteration
    mock_indevolt.set_data.reset_mock()

    # Mock call to pause (dis)charging
    await hass.services.async_call(
        BUTTON_DOMAIN,
        ButtonService.PRESS,
        {TargetKey.ENTITY_ID: ENTITY_ID_GEN2},
        blocking=True,
    )

    # Verify stop() was called and no mode switch was needed
    mock_indevolt.set_data.assert_not_called()
    mock_indevolt.stop.assert_called_once()


@pytest.mark.parametrize("generation", [2], indirect=True)
async def test_button_press_standby_rejected_command(
    hass: UniversalAssistant,
    mock_indevolt: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test standby raises UniversalAssistantError when device rejects."""
    with patch("universalassistant.components.indevolt.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    # Simulate stop() returning False (device rejected the command)
    mock_indevolt.stop.return_value = False

    # Mock call to pause (dis)charging
    with pytest.raises(UniversalAssistantError):
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {TargetKey.ENTITY_ID: ENTITY_ID_GEN2},
            blocking=True,
        )


@pytest.mark.parametrize("generation", [2], indirect=True)
async def test_button_press_standby_portable_mode_error(
    hass: UniversalAssistant,
    mock_indevolt: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test standby raises error in outdoor/portable mode."""

    # Force outdoor/portable mode
    mock_indevolt.fetch_data.return_value[IndevoltConfig.READ_ENERGY_MODE] = (
        IndevoltEnergyMode.OUTDOOR_PORTABLE
    )
    with patch("universalassistant.components.indevolt.PLATFORMS", [Platform.BUTTON]):
        await setup_integration(hass, mock_config_entry)

    # Reset mock call count for this iteration
    mock_indevolt.set_data.reset_mock()

    # Mock call to pause (dis)charging
    with pytest.raises(UniversalAssistantError) as exc_info:
        await hass.services.async_call(
            BUTTON_DOMAIN,
            ButtonService.PRESS,
            {TargetKey.ENTITY_ID: ENTITY_ID_GEN2},
            blocking=True,
        )

    # Verify correct translation key is used for the error and confirm no call was made
    assert (
        exc_info.value.translation_key
        == "energy_mode_change_unavailable_outdoor_portable"
    )
    mock_indevolt.set_data.assert_not_called()
