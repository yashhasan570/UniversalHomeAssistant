"""Test Velux switch entities."""

from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    SnapshotAssertion,
    snapshot_platform,
)
from pyvlx import PyVLXException

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import STATE_OFF, STATE_ON, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import device_registry as dr, entity_registry as er

from . import update_callback_entity

# Apply setup_integration fixture to all tests in this module
pytestmark = pytest.mark.usefixtures("setup_integration")


@pytest.fixture
def platform() -> Platform:
    """Fixture to specify platform to test."""
    return Platform.SWITCH


@pytest.mark.parametrize("mock_pyvlx", ["mock_onoff_switch"], indirect=True)
async def test_switch_setup(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    mock_pyvlx: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Snapshot the entity and validate registry metadata for switch entities."""
    await snapshot_platform(
        hass,
        entity_registry,
        snapshot,
        mock_config_entry.entry_id,
    )


async def test_switch_device_association(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    device_registry: dr.DeviceRegistry,
    mock_onoff_switch: AsyncMock,
) -> None:
    """Test switch device association."""
    test_entity_id = f"switch.{mock_onoff_switch.name.lower().replace(' ', '_')}"

    entity_entry = entity_registry.async_get(test_entity_id)
    assert entity_entry is not None
    assert entity_entry.device_id is not None
    device_entry = device_registry.async_get(entity_entry.device_id)
    assert device_entry is not None

    assert ("velux", mock_onoff_switch.serial_number) in device_entry.identifiers
    assert device_entry.name == mock_onoff_switch.name


async def test_switch_is_on(hass: __HAC_KEEP__, mock_onoff_switch: AsyncMock) -> None:
    """Test switch on state."""
    entity_id = f"switch.{mock_onoff_switch.name.lower().replace(' ', '_')}"

    # Initial state is off
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_OFF

    # Simulate switching on
    mock_onoff_switch.is_on.return_value = True
    mock_onoff_switch.is_off.return_value = False
    await update_callback_entity(hass, mock_onoff_switch)

    state = hass.states.get(entity_id)
    assert state is not None
    assert state.state == STATE_ON


async def test_switch_turn_on_off(
    hass: __HAC_KEEP__, mock_onoff_switch: AsyncMock
) -> None:
    """Test turning switch on."""
    entity_id = f"switch.{mock_onoff_switch.name.lower().replace(' ', '_')}"

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {"entity_id": entity_id},
        blocking=True,
    )
    mock_onoff_switch.set_on.assert_awaited_once()

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {"entity_id": entity_id},
        blocking=True,
    )
    mock_onoff_switch.set_off.assert_awaited_once()


@pytest.mark.parametrize("mock_pyvlx", ["mock_onoff_switch"], indirect=True)
async def test_switch_error_handling(
    hass: __HAC_KEEP__, mock_onoff_switch: AsyncMock
) -> None:
    """Test error handling when turning switching fails."""
    entity_id = f"switch.{mock_onoff_switch.name.lower().replace(' ', '_')}"
    mock_onoff_switch.set_on.side_effect = PyVLXException("Connection lost")
    mock_onoff_switch.set_off.side_effect = PyVLXException("Connection lost")

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            {"entity_id": entity_id},
            blocking=True,
        )

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_OFF,
            {"entity_id": entity_id},
            blocking=True,
        )
