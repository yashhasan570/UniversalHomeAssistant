"""Test for the SmartThings update platform."""

from unittest.mock import AsyncMock

from pysmartthings import Attribute, Capability, Command
from pysmartthings.models import HealthStatus
import pytest
from pytest_universalassistant.common import MockConfigEntry
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.smartthings.const import MAIN
from universalassistant.components.update import (
    ATTR_IN_PROGRESS,
    DOMAIN as UPDATE_DOMAIN,
    UpdateService,
)
from universalassistant.const import (
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    CommonServiceArgument,
    Platform,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er

from . import (
    setup_integration,
    snapshot_smartthings_entities,
    trigger_health_update,
    trigger_update,
)


async def test_all_entities(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
) -> None:
    """Test all entities."""
    await setup_integration(hass, mock_config_entry)

    snapshot_smartthings_entities(hass, entity_registry, snapshot, Platform.UPDATE)


@pytest.mark.parametrize("device_fixture", ["contact_sensor"])
async def test_installing_update(
    hass: __HAC_KEEP__,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test installing an update."""
    await setup_integration(hass, mock_config_entry)

    await hass.services.async_call(
        UPDATE_DOMAIN,
        UpdateService.INSTALL,
        {
            CommonServiceArgument.ENTITY_ID: "update.theater_front_door_open_closed_sensor_firmware"
        },
        blocking=True,
    )
    devices.execute_device_command.assert_called_once_with(
        "2d9a892b-1c93-45a5-84cb-0e81889498c6",
        Capability.FIRMWARE_UPDATE,
        Command.UPDATE_FIRMWARE,
        MAIN,
    )


@pytest.mark.parametrize("device_fixture", ["contact_sensor"])
async def test_state_update(
    hass: __HAC_KEEP__,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test state update."""
    await setup_integration(hass, mock_config_entry)

    assert (
        hass.states.get("update.theater_front_door_open_closed_sensor_firmware").state
        == STATE_ON
    )

    await trigger_update(
        hass,
        devices,
        "2d9a892b-1c93-45a5-84cb-0e81889498c6",
        Capability.FIRMWARE_UPDATE,
        Attribute.CURRENT_VERSION,
        "00000104",
    )

    assert (
        hass.states.get("update.theater_front_door_open_closed_sensor_firmware").state
        == STATE_OFF
    )


@pytest.mark.parametrize("device_fixture", ["contact_sensor"])
async def test_state_progress_update(
    hass: __HAC_KEEP__,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test state progress update."""
    await setup_integration(hass, mock_config_entry)

    assert (
        hass.states.get(
            "update.theater_front_door_open_closed_sensor_firmware"
        ).attributes[ATTR_IN_PROGRESS]
        is False
    )

    await trigger_update(
        hass,
        devices,
        "2d9a892b-1c93-45a5-84cb-0e81889498c6",
        Capability.FIRMWARE_UPDATE,
        Attribute.STATE,
        "updateInProgress",
    )

    assert (
        hass.states.get(
            "update.theater_front_door_open_closed_sensor_firmware"
        ).attributes[ATTR_IN_PROGRESS]
        is True
    )


@pytest.mark.parametrize("device_fixture", ["centralite"])
async def test_state_update_available(
    hass: __HAC_KEEP__,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test state update available."""
    await setup_integration(hass, mock_config_entry)

    assert hass.states.get("update.theater_dimmer_debian_firmware").state == STATE_OFF

    await trigger_update(
        hass,
        devices,
        "d0268a69-abfb-4c92-a646-61cec2e510ad",
        Capability.FIRMWARE_UPDATE,
        Attribute.AVAILABLE_VERSION,
        "16015011",
    )

    assert hass.states.get("update.theater_dimmer_debian_firmware").state == STATE_ON


@pytest.mark.parametrize("device_fixture", ["centralite"])
async def test_availability(
    hass: __HAC_KEEP__,
    devices: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test availability."""
    await setup_integration(hass, mock_config_entry)

    assert hass.states.get("update.theater_dimmer_debian_firmware").state == STATE_OFF

    await trigger_health_update(
        hass, devices, "d0268a69-abfb-4c92-a646-61cec2e510ad", HealthStatus.OFFLINE
    )

    assert (
        hass.states.get("update.theater_dimmer_debian_firmware").state
        == STATE_UNAVAILABLE
    )

    await trigger_health_update(
        hass, devices, "d0268a69-abfb-4c92-a646-61cec2e510ad", HealthStatus.ONLINE
    )

    assert hass.states.get("update.theater_dimmer_debian_firmware").state == STATE_OFF


@pytest.mark.parametrize("device_fixture", ["centralite"])
async def test_availability_at_start(
    hass: __HAC_KEEP__,
    unavailable_device: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test unavailable at boot."""
    await setup_integration(hass, mock_config_entry)
    assert (
        hass.states.get("update.theater_dimmer_debian_firmware").state
        == STATE_UNAVAILABLE
    )
