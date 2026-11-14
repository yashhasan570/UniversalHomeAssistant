"""Tests for the Flexit Nordic (BACnet) switch entities."""

from unittest.mock import AsyncMock

from flexit_bacnet import DecodingError
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN, SwitchService
from universalassistant.const import STATE_OFF, STATE_ON, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import entity_registry as er

from . import setup_with_selected_platforms

ENTITY_ID = "switch.device_name_electric_heater"


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_switches(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_flexit_bacnet: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test switch states are correctly collected from library."""

    await setup_with_selected_platforms(hass, mock_config_entry, [Platform.SWITCH])

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_switches_implementation(
    hass: __HAC_KEEP__,
    snapshot: SnapshotAssertion,
    entity_registry: er.EntityRegistry,
    mock_flexit_bacnet: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test that the switch can be turned on and off."""

    await setup_with_selected_platforms(hass, mock_config_entry, [Platform.SWITCH])
    assert hass.states.get(ENTITY_ID) == snapshot(name=f"{ENTITY_ID}-state")

    # Set to off
    mock_flexit_bacnet.electric_heater = False

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {CommonServiceArgument.ENTITY_ID: ENTITY_ID},
        blocking=True,
    )

    mocked_method = mock_flexit_bacnet.disable_electric_heater
    assert len(mocked_method.mock_calls) == 1
    assert hass.states.get(ENTITY_ID).state == STATE_OFF

    # Set to on
    mock_flexit_bacnet.electric_heater = True

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: ENTITY_ID},
        blocking=True,
    )

    mocked_method = mock_flexit_bacnet.enable_electric_heater
    assert len(mocked_method.mock_calls) == 1
    assert hass.states.get(ENTITY_ID).state == STATE_ON

    # Error recovery, when turning off
    mock_flexit_bacnet.disable_electric_heater.side_effect = DecodingError

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_OFF,
            {CommonServiceArgument.ENTITY_ID: ENTITY_ID},
            blocking=True,
        )

    mocked_method = mock_flexit_bacnet.disable_electric_heater
    assert len(mocked_method.mock_calls) == 2

    mock_flexit_bacnet.disable_electric_heater.side_effect = None
    mock_flexit_bacnet.electric_heater = False

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_OFF,
        {CommonServiceArgument.ENTITY_ID: ENTITY_ID},
        blocking=True,
    )

    assert hass.states.get(ENTITY_ID).state == STATE_OFF

    # Error recovery, when turning on
    mock_flexit_bacnet.enable_electric_heater.side_effect = DecodingError

    with pytest.raises(__HAC_KEEP__Error):
        await hass.services.async_call(
            SWITCH_DOMAIN,
            SwitchService.TURN_ON,
            {CommonServiceArgument.ENTITY_ID: ENTITY_ID},
            blocking=True,
        )

    mocked_method = mock_flexit_bacnet.enable_electric_heater
    assert len(mocked_method.mock_calls) == 2

    mock_flexit_bacnet.enable_electric_heater.side_effect = None
    mock_flexit_bacnet.electric_heater = True

    await hass.services.async_call(
        SWITCH_DOMAIN,
        SwitchService.TURN_ON,
        {CommonServiceArgument.ENTITY_ID: ENTITY_ID},
        blocking=True,
    )

    assert hass.states.get(ENTITY_ID).state == STATE_ON
