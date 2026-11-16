"""Test Yellow beta firmware switch entity."""

from unittest.mock import Mock, call, patch

from ha_silabs_firmware_client import FirmwareManifest, FirmwareMetadata
import pytest
from pytest_universalassistant.common import MockConfigEntry, mock_restore_cache
from yarl import URL

from universalassistant.components.universalassistant_yellow.const import DOMAIN, RADIO_DEVICE
from universalassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from universalassistant.const import (
    ATTR_ENTITY_ID,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)
from universalassistant.core import UniversalAssistant, State
from universalassistant.setup import async_setup_component
from universalassistant.util import dt as dt_util

SWITCH_ENTITY_ID = "switch.universal_assistant_yellow_radio_beta_firmware_updates"

TEST_MANIFEST = FirmwareManifest(
    url=URL("https://example.org/firmware"),
    html_url=URL("https://example.org/release_notes"),
    created_at=dt_util.utcnow(),
    firmwares=(
        FirmwareMetadata(
            filename="skyconnect_zigbee_ncp_test.gbl",
            checksum="aaa",
            size=123,
            release_notes="Some release notes go here",
            metadata={
                "baudrate": 115200,
                "ezsp_version": "7.4.4.0",
                "fw_type": "zigbee_ncp",
                "fw_variant": None,
                "metadata_version": 2,
                "sdk_version": "4.4.4",
            },
            url=URL("https://example.org/firmwares/skyconnect_zigbee_ncp_test.gbl"),
        ),
    ),
)


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
@pytest.mark.parametrize(
    ("service", "target_state", "expected_prerelease"),
    [
        (SERVICE_TURN_ON, STATE_ON, True),
        (SERVICE_TURN_OFF, STATE_OFF, False),
    ],
)
async def test_switch_turn_on_off(
    hass: UniversalAssistant,
    service: str,
    target_state: str,
    expected_prerelease: bool,
) -> None:
    """Test turning switch on/off updates state and coordinator."""
    await async_setup_component(hass, "universalassistant", {})

    # Start with opposite state
    mock_restore_cache(
        hass,
        [
            State(
                SWITCH_ENTITY_ID,
                STATE_ON if service == SERVICE_TURN_OFF else STATE_OFF,
            )
        ],
    )

    # Set up the Yellow integration
    yellow_config_entry = MockConfigEntry(
        title="Universal Home Assistant Yellow",
        domain=DOMAIN,
        data={
            "firmware": "ezsp",
            "firmware_version": "7.3.1.0 build 0",
            "device": RADIO_DEVICE,
        },
        version=1,
        minor_version=3,
    )
    yellow_config_entry.add_to_hass(hass)

    with (
        patch(
            "universalassistant.components.universalassistant_yellow.is_hassio", return_value=True
        ),
        patch(
            "universalassistant.components.universalassistant_yellow.get_os_info",
            return_value={"board": "yellow"},
        ),
        patch(
            "universalassistant.components.universalassistant_hardware.coordinator.FirmwareUpdateClient"
        ) as mock_client,
        patch(
            "universalassistant.components.universalassistant_hardware.coordinator.FirmwareUpdateCoordinator.async_refresh"
        ) as mock_refresh,
    ):
        mock_client.return_value.async_update_data.return_value = TEST_MANIFEST
        mock_client.return_value.update_prerelease = Mock()

        assert await hass.config_entries.async_setup(yellow_config_entry.entry_id)
        await hass.async_block_till_done()

        # Reset mocks after setup
        mock_client.return_value.update_prerelease.reset_mock()
        mock_refresh.reset_mock()

        # Call the service
        await hass.services.async_call(
            SWITCH_DOMAIN,
            service,
            {ATTR_ENTITY_ID: SWITCH_ENTITY_ID},
            blocking=True,
        )

        # Verify state changed
        state = hass.states.get(SWITCH_ENTITY_ID)
        assert state is not None
        assert state.state == target_state

        # Verify coordinator methods were called
        assert mock_client.return_value.update_prerelease.mock_calls == [
            call(expected_prerelease)
        ]
        assert len(mock_refresh.mock_calls) == 1
