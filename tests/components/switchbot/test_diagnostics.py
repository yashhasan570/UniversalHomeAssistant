"""Tests for the diagnostics data provided by the Switchbot integration."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.bluetooth import inject_bluetooth_service_info
from pytest_universalassistant.components.diagnostics import get_diagnostics_for_config_entry
from pytest_universalassistant.typing import ClientSessionGenerator
from syrupy.assertion import SnapshotAssertion
from syrupy.filters import props

from universalassistant.components.switchbot.const import (
    CONF_ENCRYPTION_KEY,
    CONF_KEY_ID,
    CONF_RETRY_COUNT,
    DEFAULT_RETRY_COUNT,
    DOMAIN,
)
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import CONF_ADDRESS, CONF_NAME, CONF_SENSOR_TYPE
from universalassistant.core import __HAC_KEEP__

from . import WORELAY_SWITCH_1PM_SERVICE_INFO


async def test_diagnostics(
    hass: __HAC_KEEP__,
    hass_client: ClientSessionGenerator,
    snapshot: SnapshotAssertion,
) -> None:
    """Test diagnostics for config entry."""

    inject_bluetooth_service_info(hass, WORELAY_SWITCH_1PM_SERVICE_INFO)

    with patch(
        "universalassistant.components.switchbot.switch.switchbot.SwitchbotRelaySwitch.update",
        return_value=None,
    ):
        mock_config_entry = MockConfigEntry(
            domain=DOMAIN,
            data={
                CONF_ADDRESS: "aa:bb:cc:dd:ee:ff",
                CONF_NAME: "test-name",
                CONF_SENSOR_TYPE: "relay_switch_1pm",
                CONF_KEY_ID: "ff",
                CONF_ENCRYPTION_KEY: "ffffffffffffffffffffffffffffffff",
            },
            unique_id="aabbccddeeaa",
            options={CONF_RETRY_COUNT: DEFAULT_RETRY_COUNT},
        )
        mock_config_entry.add_to_hass(hass)

        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()
        assert mock_config_entry.state is ConfigEntryState.LOADED

    result = await get_diagnostics_for_config_entry(
        hass, hass_client, mock_config_entry
    )
    assert result == snapshot(
        exclude=props("created_at", "modified_at", "entry_id", "time")
    )
