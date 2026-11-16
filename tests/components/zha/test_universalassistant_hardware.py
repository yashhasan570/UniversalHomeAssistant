"""Test Universal Home Assistant Hardware platform for ZHA."""

from unittest.mock import MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from zigpy.application import ControllerApplication

from universalassistant.components.universalassistant_hardware import (
    DOMAIN as HOMEASSISTANT_HARDWARE_DOMAIN,
)
from universalassistant.components.universalassistant_hardware.helpers import (
    async_register_firmware_info_callback,
)
from universalassistant.components.universalassistant_hardware.util import (
    ApplicationType,
    FirmwareInfo,
    OwningIntegration,
)
from universalassistant.components.zha import DOMAIN
from universalassistant.components.zha.universalassistant_hardware import get_firmware_info
from universalassistant.config_entries import ConfigEntryState
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


async def test_get_firmware_info_normal(hass: UniversalAssistant) -> None:
    """Test `get_firmware_info`."""

    zha = MockConfigEntry(
        domain=DOMAIN,
        unique_id="some_unique_id",
        data={
            "device": {
                "path": "/dev/ttyUSB1",
                "baudrate": 115200,
                "flow_control": None,
            },
            "radio_type": "ezsp",
        },
        version=5,
    )
    zha.add_to_hass(hass)
    zha.mock_state(hass, ConfigEntryState.LOADED)

    # With ZHA running
    with patch(
        "universalassistant.components.zha.universalassistant_hardware.get_zha_gateway"
    ) as mock_get_zha_gateway:
        mock_get_zha_gateway.return_value.state.node_info.version = "1.2.3.4"
        fw_info_running = get_firmware_info(hass, zha)

    assert fw_info_running == FirmwareInfo(
        device="/dev/ttyUSB1",
        firmware_type=ApplicationType.EZSP,
        firmware_version="1.2.3.4",
        source="zha",
        owners=[OwningIntegration(config_entry_id=zha.entry_id)],
    )
    assert await fw_info_running.is_running(hass) is True

    # With ZHA not running
    zha.mock_state(hass, ConfigEntryState.NOT_LOADED)
    fw_info_not_running = get_firmware_info(hass, zha)

    assert fw_info_not_running == FirmwareInfo(
        device="/dev/ttyUSB1",
        firmware_type=ApplicationType.EZSP,
        firmware_version=None,
        source="zha",
        owners=[OwningIntegration(config_entry_id=zha.entry_id)],
    )
    assert await fw_info_not_running.is_running(hass) is False


@pytest.mark.parametrize(
    "data",
    [
        # Missing data
        {},
        # Bad radio type
        {"device": {"path": "/dev/ttyUSB1"}, "radio_type": "znp"},
    ],
)
async def test_get_firmware_info_errors(
    hass: UniversalAssistant, data: dict[str, str | int | None]
) -> None:
    """Test `get_firmware_info` with config entry data format errors."""
    zha = MockConfigEntry(
        domain=DOMAIN,
        unique_id="some_unique_id",
        data=data,
        version=5,
    )
    zha.add_to_hass(hass)

    assert (get_firmware_info(hass, zha)) is None


async def test_hardware_firmware_info_provider_notification(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    mock_zigpy_connect: ControllerApplication,
) -> None:
    """Test that the ZHA gateway provides hardware and firmware information."""
    config_entry.add_to_hass(hass)

    await async_setup_component(hass, HOMEASSISTANT_HARDWARE_DOMAIN, {})

    callback = MagicMock()
    async_register_firmware_info_callback(hass, "/dev/ttyUSB0", callback)

    await hass.config_entries.async_setup(config_entry.entry_id)

    callback.assert_called_once_with(
        FirmwareInfo(
            device="/dev/ttyUSB0",
            firmware_type=ApplicationType.EZSP,
            firmware_version="7.1.4.0 build 389",
            source="zha",
            owners=[OwningIntegration(config_entry_id=config_entry.entry_id)],
        )
    )
