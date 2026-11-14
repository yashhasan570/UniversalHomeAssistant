"""Tests for the Lutron select platform."""

from unittest.mock import MagicMock, patch

from pylutron import Led
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import STATE_UNKNOWN, CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er


@pytest.fixture(autouse=True)
def setup_platforms():
    """Patch PLATFORMS for all tests in this file."""
    with patch("universalassistant.components.lutron.PLATFORMS", [Platform.SELECT]):
        yield


async def test_led_select_setup(
    hass: __HAC_KEEP__,
    mock_lutron: MagicMock,
    mock_config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the setup of Lutron LED select entities."""
    mock_config_entry.add_to_hass(hass)

    led = mock_lutron.areas[0].keypads[0].leds[0]
    led.last_state = Led.LED_OFF

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_led_select_option(
    hass: __HAC_KEEP__, mock_lutron: MagicMock, mock_config_entry: MockConfigEntry
) -> None:
    """Test selecting an option for a Lutron LED select entity."""
    mock_config_entry.add_to_hass(hass)

    led = mock_lutron.areas[0].keypads[0].leds[0]

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = "select.test_keypad_test_button_led"

    # Select "on"
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: entity_id,
            SelectServiceArgument.OPTION: "on",
        },
        blocking=True,
    )
    assert led.state == Led.LED_ON

    # Select "slow_flash"
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: entity_id,
            SelectServiceArgument.OPTION: "slow_flash",
        },
        blocking=True,
    )
    assert led.state == Led.LED_SLOW_FLASH

    # Select "fast_flash"
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: entity_id,
            SelectServiceArgument.OPTION: "fast_flash",
        },
        blocking=True,
    )
    assert led.state == Led.LED_FAST_FLASH

    # Select "off"
    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: entity_id,
            SelectServiceArgument.OPTION: "off",
        },
        blocking=True,
    )
    assert led.state == Led.LED_OFF


async def test_led_select_update(
    hass: __HAC_KEEP__, mock_lutron: MagicMock, mock_config_entry: MockConfigEntry
) -> None:
    """Test LED state update from library."""
    mock_config_entry.add_to_hass(hass)

    led = mock_lutron.areas[0].keypads[0].leds[0]
    led.last_state = Led.LED_OFF

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    entity_id = "select.test_keypad_test_button_led"
    assert hass.states.get(entity_id).state == "off"

    # Simulate update from library
    led.last_state = Led.LED_SLOW_FLASH
    callback = led.subscribe.call_args[0][0]
    callback(led, None, None, {})
    await hass.async_block_till_done()

    assert hass.states.get(entity_id).state == "slow_flash"


async def test_led_select_unknown_state(
    hass: __HAC_KEEP__, mock_lutron: MagicMock, mock_config_entry: MockConfigEntry
) -> None:
    """Test handling of unknown LED state from pylutron."""
    mock_config_entry.add_to_hass(hass)

    led = mock_lutron.areas[0].keypads[0].leds[0]
    led.last_state = 99  # Unknown state

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get("select.test_keypad_test_button_led")
    assert state is not None
    assert state.state == STATE_UNKNOWN
