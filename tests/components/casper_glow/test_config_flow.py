"""Test the Casper Glow config flow."""

from unittest.mock import MagicMock, patch

from bluetooth_data_tools import human_readable_name
from pycasperglow import CasperGlowError
import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.bluetooth import (
    generate_advertisement_data,
    generate_ble_device,
    inject_bluetooth_service_info,
)

from universalassistant.components.bluetooth import BluetoothServiceInfoBleak
from universalassistant.components.casper_glow.const import DOMAIN
from universalassistant.config_entries import SOURCE_BLUETOOTH, SOURCE_USER
from universalassistant.const import CONF_ADDRESS
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.helpers.device_registry import format_mac

from . import (
    CASPER_GLOW_DISCOVERY_INFO,
    NOT_CASPER_GLOW_DISCOVERY_INFO,
    SAMSUNG_EARBUDS_DISCOVERY_INFO,
)


async def test_bluetooth_step_success(
    hass: __HAC_KEEP__, mock_casper_glow: MagicMock
) -> None:
    """Test bluetooth discovery step success."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_BLUETOOTH},
        data=CASPER_GLOW_DISCOVERY_INFO,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"

    # Inject before configure so async_setup_entry can find the device via
    # async_ble_device_from_address. The unique_id is already claimed by our
    # flow so the BT manager's auto-started flow will abort as a duplicate.
    inject_bluetooth_service_info(hass, CASPER_GLOW_DISCOVERY_INFO)

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == human_readable_name(
        None, CASPER_GLOW_DISCOVERY_INFO.name, CASPER_GLOW_DISCOVERY_INFO.address
    )
    assert result["data"] == {
        CONF_ADDRESS: CASPER_GLOW_DISCOVERY_INFO.address,
    }
    assert result["result"].unique_id == format_mac(CASPER_GLOW_DISCOVERY_INFO.address)


@pytest.mark.parametrize(
    ("side_effect", "reason"),
    [(CasperGlowError, "cannot_connect"), (RuntimeError, "unknown")],
)
async def test_bluetooth_confirm_error(
    hass: __HAC_KEEP__,
    side_effect: type[Exception],
    reason: str,
) -> None:
    """Test bluetooth confirm step error handling."""
    with patch(
        "universalassistant.components.casper_glow.config_flow.CasperGlow.handshake",
        side_effect=side_effect,
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": SOURCE_BLUETOOTH},
            data=CASPER_GLOW_DISCOVERY_INFO,
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == reason


async def test_bluetooth_step_ignores_unrecognized_device(
    hass: __HAC_KEEP__, mock_casper_glow: MagicMock
) -> None:
    """Test bluetooth discovery aborts before handshaking with unsupported devices."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_BLUETOOTH},
        data=SAMSUNG_EARBUDS_DISCOVERY_INFO,
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "not_supported"
    mock_casper_glow.handshake.assert_not_called()


async def test_user_step_success(
    hass: __HAC_KEEP__, mock_casper_glow: MagicMock
) -> None:
    """Test user step success path."""
    with patch(
        "universalassistant.components.casper_glow.config_flow.async_discovered_service_info",
        return_value=[NOT_CASPER_GLOW_DISCOVERY_INFO, CASPER_GLOW_DISCOVERY_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    # Inject before configure so async_setup_entry can find the device via
    # async_ble_device_from_address.
    inject_bluetooth_service_info(hass, CASPER_GLOW_DISCOVERY_INFO)

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_ADDRESS: CASPER_GLOW_DISCOVERY_INFO.address,
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == human_readable_name(
        None, CASPER_GLOW_DISCOVERY_INFO.name, CASPER_GLOW_DISCOVERY_INFO.address
    )
    assert result["data"] == {
        CONF_ADDRESS: CASPER_GLOW_DISCOVERY_INFO.address,
    }
    assert result["result"].unique_id == format_mac(CASPER_GLOW_DISCOVERY_INFO.address)


async def test_user_step_no_devices(hass: __HAC_KEEP__) -> None:
    """Test user step with no devices found."""
    with patch(
        "universalassistant.components.casper_glow.config_flow.async_discovered_service_info",
        return_value=[NOT_CASPER_GLOW_DISCOVERY_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


@pytest.mark.parametrize(
    ("side_effect", "expected_error"),
    [(CasperGlowError, "cannot_connect"), (RuntimeError, "unknown")],
)
async def test_user_step_error(
    hass: __HAC_KEEP__,
    side_effect: type[Exception],
    expected_error: str,
) -> None:
    """Test user step error handling."""
    with patch(
        "universalassistant.components.casper_glow.config_flow.async_discovered_service_info",
        return_value=[CASPER_GLOW_DISCOVERY_INFO],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    with patch(
        "universalassistant.components.casper_glow.config_flow.CasperGlow.handshake",
        side_effect=side_effect,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_ADDRESS: CASPER_GLOW_DISCOVERY_INFO.address},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": expected_error}

    with (
        patch("universalassistant.components.casper_glow.config_flow.CasperGlow.handshake"),
        patch(
            "universalassistant.components.casper_glow.async_setup_entry",
            return_value=None,
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_ADDRESS: CASPER_GLOW_DISCOVERY_INFO.address},
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_already_configured(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test already configured device."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_BLUETOOTH},
        data=CASPER_GLOW_DISCOVERY_INFO,
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_user_step_skips_unrecognized_device(hass: __HAC_KEEP__) -> None:
    """Test that devices without a matching local name prefix are skipped."""
    unrecognized_discovery = BluetoothServiceInfoBleak(
        name="",
        address="AA:BB:CC:DD:EE:11",
        rssi=-60,
        manufacturer_data={},
        service_uuids=[],
        service_data={},
        source="local",
        device=generate_ble_device(address="AA:BB:CC:DD:EE:11", name=""),
        advertisement=generate_advertisement_data(service_uuids=[]),
        time=0,
        connectable=True,
        tx_power=-127,
    )
    with patch(
        "universalassistant.components.casper_glow.config_flow.async_discovered_service_info",
        return_value=[unrecognized_discovery],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_USER}
        )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"
