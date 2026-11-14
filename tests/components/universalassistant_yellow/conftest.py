"""Test fixtures for the Universal Universal Home Assistant Yellow integration."""

from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def mock_zha_config_flow_setup() -> Generator[None]:
    """Mock the radio connection and probing of the ZHA config flow."""

    def mock_probe(config: dict[str, Any]) -> dict[str, Any]:
        # The radio probing will return the correct baudrate
        return {**config, "baudrate": 115200}

    mock_connect_app = MagicMock()
    mock_connect_app.__aenter__.return_value.backups.backups = [MagicMock()]
    mock_connect_app.__aenter__.return_value.backups.create_backup.return_value = (
        MagicMock()
    )

    with (
        patch(
            "bellows.zigbee.application.ControllerApplication.probe",
            side_effect=mock_probe,
        ),
        patch(
            "universalassistant.components.zha.radio_manager.ZhaRadioManager.create_zigpy_app",
            return_value=mock_connect_app,
        ),
        patch(
            "universalassistant.components.zha.async_setup_entry",
            return_value=None,
        ),
    ):
        yield


@pytest.fixture(autouse=True)
def mock_zha_get_last_network_settings() -> Generator[None]:
    """Mock zha.api.async_get_last_network_settings."""

    with patch(
        "universalassistant.components.zha.api.async_get_last_network_settings",
        AsyncMock(return_value=None),
    ):
        yield


@pytest.fixture(autouse=True)
def mock_firmware_update_client() -> Generator[MagicMock]:
    """Mock the FirmwareUpdateClient to avoid network requests."""
    with patch(
        "universalassistant.components.universalassistant_hardware.coordinator.FirmwareUpdateClient",
        autospec=True,
    ) as mock_client:
        mock_client.return_value.async_update_data = AsyncMock(return_value=None)
        yield mock_client


@pytest.fixture(autouse=True)
def mock_rpi_firmware_info() -> Generator[AsyncMock]:
    """Skip the Raspberry Pi EEPROM firmware probe by default.

    Tests that exercise the EEPROM update entity can override the return value.
    """
    with patch(
        "universalassistant.components.universalassistant_yellow.update."
        "async_get_raspberry_pi_firmware_info",
        return_value=None,
    ) as mock_info:
        yield mock_info
