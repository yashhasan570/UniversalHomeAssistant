"""Test the config flow for the Insteon integration."""

from collections.abc import Callable
from typing import Any
from unittest.mock import AsyncMock, patch

from probatio import to_field_list
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.insteon.config_flow import (
    STEP_HUB_V1,
    STEP_HUB_V2,
    STEP_PLM,
    STEP_PLM_MANUALLY,
)
from universalassistant.components.insteon.const import CONF_HUB_VERSION, DOMAIN
from universalassistant.config_entries import ConfigFlowResult
from universalassistant.const import CONF_DEVICE, CONF_HOST
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.helpers.service_info.dhcp import DhcpServiceInfo
from universalassistant.helpers.service_info.usb import UsbServiceInfo

from .const import (
    MOCK_DEVICE,
    MOCK_USER_INPUT_HUB_V1,
    MOCK_USER_INPUT_HUB_V2,
    MOCK_USER_INPUT_PLM,
    MOCK_USER_INPUT_PLM_MANUAL,
    PATCH_ASYNC_SETUP_ENTRY,
    PATCH_CONNECTION,
    PATCH_USB_LIST,
)

USB_PORTS = {"/dev/ttyUSB0": "/dev/ttyUSB0", MOCK_DEVICE: MOCK_DEVICE}


async def mock_successful_connection(*args, **kwargs):
    """Return a successful connection."""
    return True


async def mock_usb_list(hass: UniversalAssistant):
    """Return a mock list of USB devices."""
    return USB_PORTS


@pytest.fixture(autouse=True)
def patch_usb_list():
    """Only setup the lock and required base platforms to speed up tests."""
    with patch(
        PATCH_USB_LIST,
        mock_usb_list,
    ):
        yield


async def mock_failed_connection(*args, **kwargs):
    """Return a failed connection."""
    raise ConnectionError("Connection failed")


async def _init_form(hass: UniversalAssistant, modem_type: str) -> ConfigFlowResult:
    """Run the user form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.MENU

    return await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"next_step_id": modem_type},
    )


async def _device_form(
    hass: UniversalAssistant,
    flow_id: str,
    connection: Callable[..., Any],
    user_input: dict[str, Any] | None,
) -> tuple[ConfigFlowResult, AsyncMock]:
    """Test the PLM, Hub v1 or Hub v2 form."""
    with (
        patch(
            PATCH_CONNECTION,
            new=connection,
        ),
        patch(
            PATCH_ASYNC_SETUP_ENTRY,
            return_value=None,
        ) as mock_setup_entry,
    ):
        result = await hass.config_entries.flow.async_configure(flow_id, user_input)
        await hass.async_block_till_done()
    return result, mock_setup_entry


async def test_form_select_modem(hass: UniversalAssistant) -> None:
    """Test we get a modem form."""

    result = await _init_form(hass, STEP_HUB_V2)
    assert result["step_id"] == STEP_HUB_V2
    assert result["type"] is FlowResultType.FORM


async def test_fail_on_existing(hass: UniversalAssistant) -> None:
    """Test we fail if the integration is already configured."""
    MockConfigEntry(domain=DOMAIN).add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"


async def test_form_select_plm(hass: UniversalAssistant) -> None:
    """Test we set up the PLM correctly."""

    result = await _init_form(hass, STEP_PLM)

    result2, mock_setup_entry = await _device_form(
        hass, result["flow_id"], mock_successful_connection, MOCK_USER_INPUT_PLM
    )
    # pylint: disable-next=universal-assistant-tests-config-flow-unique-id
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["data"] == MOCK_USER_INPUT_PLM

    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_select_plm_no_usb(hass: UniversalAssistant) -> None:
    """Test we set up the PLM when no comm ports are found."""

    temp_usb_list = dict(USB_PORTS)
    USB_PORTS.clear()
    result = await _init_form(hass, STEP_PLM)

    result2, _ = await _device_form(
        hass, result["flow_id"], mock_successful_connection, None
    )
    USB_PORTS.update(temp_usb_list)
    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == STEP_PLM_MANUALLY


async def test_form_select_plm_manual(hass: UniversalAssistant) -> None:
    """Test we set up the PLM correctly."""

    result = await _init_form(hass, STEP_PLM)

    result2, mock_setup_entry = await _device_form(
        hass, result["flow_id"], mock_failed_connection, MOCK_USER_INPUT_PLM_MANUAL
    )

    result3, mock_setup_entry = await _device_form(
        hass, result2["flow_id"], mock_successful_connection, MOCK_USER_INPUT_PLM
    )
    assert result2["type"] is FlowResultType.FORM
    # pylint: disable-next=universal-assistant-tests-config-flow-unique-id
    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["data"] == MOCK_USER_INPUT_PLM

    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_select_hub_v1(hass: UniversalAssistant) -> None:
    """Test we set up the Hub v1 correctly."""

    result = await _init_form(hass, STEP_HUB_V1)

    result2, mock_setup_entry = await _device_form(
        hass, result["flow_id"], mock_successful_connection, MOCK_USER_INPUT_HUB_V1
    )
    # pylint: disable-next=universal-assistant-tests-config-flow-unique-id
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["data"] == {
        **MOCK_USER_INPUT_HUB_V1,
        CONF_HUB_VERSION: 1,
    }

    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_select_hub_v2(hass: UniversalAssistant) -> None:
    """Test we set up the Hub v2 correctly."""

    result = await _init_form(hass, STEP_HUB_V2)

    result2, mock_setup_entry = await _device_form(
        hass, result["flow_id"], mock_successful_connection, MOCK_USER_INPUT_HUB_V2
    )
    # pylint: disable-next=universal-assistant-tests-config-flow-unique-id
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["data"] == {
        **MOCK_USER_INPUT_HUB_V2,
        CONF_HUB_VERSION: 2,
    }

    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_discovery_dhcp(hass: UniversalAssistant) -> None:
    """Test the discovery of the Hub via DHCP."""
    discovery_info = DhcpServiceInfo("1.2.3.4", "", "aabbccddeeff")
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_DHCP}, data=discovery_info
    )
    assert result["type"] is FlowResultType.MENU

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {"next_step_id": STEP_HUB_V2},
    )
    assert result2["type"] is FlowResultType.FORM
    schema = to_field_list(result2["data_schema"])
    found_host = False
    for field in schema:
        if field["name"] == CONF_HOST:
            assert field["default"] == "1.2.3.4"
            found_host = True
    assert found_host


async def test_failed_connection_plm(hass: UniversalAssistant) -> None:
    """Test a failed connection with the PLM."""

    result = await _init_form(hass, STEP_PLM)

    result2, _ = await _device_form(
        hass, result["flow_id"], mock_failed_connection, MOCK_USER_INPUT_PLM
    )
    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}

    result3, _ = await _device_form(
        hass, result2["flow_id"], mock_successful_connection, MOCK_USER_INPUT_PLM
    )
    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_failed_connection_plm_manually(hass: UniversalAssistant) -> None:
    """Test a failed connection with the PLM."""

    result = await _init_form(hass, STEP_PLM)

    _result2, _ = await _device_form(
        hass, result["flow_id"], mock_successful_connection, MOCK_USER_INPUT_PLM_MANUAL
    )
    result3, _ = await _device_form(
        hass, result["flow_id"], mock_failed_connection, MOCK_USER_INPUT_PLM
    )
    assert result3["type"] is FlowResultType.FORM
    assert result3["errors"] == {"base": "cannot_connect"}

    result4, _ = await _device_form(
        hass, result3["flow_id"], mock_successful_connection, MOCK_USER_INPUT_PLM
    )
    assert result4["type"] is FlowResultType.CREATE_ENTRY


async def test_failed_connection_hub(hass: UniversalAssistant) -> None:
    """Test a failed connection with a Hub."""

    result = await _init_form(hass, STEP_HUB_V2)

    result2, _ = await _device_form(
        hass, result["flow_id"], mock_failed_connection, MOCK_USER_INPUT_HUB_V2
    )
    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}

    result3, _ = await _device_form(
        hass, result2["flow_id"], mock_successful_connection, MOCK_USER_INPUT_HUB_V2
    )
    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_discovery_via_usb(hass: UniversalAssistant) -> None:
    """Test usb flow."""
    discovery_info = UsbServiceInfo(
        device="/dev/ttyINSTEON",
        pid="AAAA",
        vid="AAAA",
        serial_number="1234",
        description="insteon radio",
        manufacturer="test",
    )
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USB}, data=discovery_info
    )
    await hass.async_block_till_done()
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "confirm_usb"

    with patch(PATCH_CONNECTION):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
        await hass.async_block_till_done()

    # pylint: disable-next=universal-assistant-tests-config-flow-unique-id
    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["data"] == {"device": "/dev/ttyINSTEON"}


async def test_discovery_via_usb_already_setup(hass: UniversalAssistant) -> None:
    """Test usb flow -- already setup."""

    MockConfigEntry(
        domain=DOMAIN, data={CONF_DEVICE: {CONF_DEVICE: "/dev/ttyUSB1"}}
    ).add_to_hass(hass)

    discovery_info = UsbServiceInfo(
        device="/dev/ttyINSTEON",
        pid="AAAA",
        vid="AAAA",
        serial_number="1234",
        description="insteon radio",
        manufacturer="test",
    )
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USB}, data=discovery_info
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"
