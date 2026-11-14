"""Test the ToGrill config flow."""

from unittest.mock import Mock, patch

from bleak.exc import BleakError
import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.bluetooth import inject_bluetooth_service_info

from universalassistant import config_entries
from universalassistant.components.togrill.const import DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from . import TOGRILL_SERVICE_INFO, TOGRILL_SERVICE_INFO_NO_NAME, setup_entry

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def test_user_selection(
    hass: __HAC_KEEP__,
) -> None:
    """Test we can select a device."""

    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO)
    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO_NO_NAME)
    await hass.async_block_till_done(wait_background_tasks=True)

    with patch(
        "universalassistant.components.togrill.config_flow.bluetooth.async_request_active_scan"
    ) as mock_request_active_scan:
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    mock_request_active_scan.assert_awaited_once_with(hass)

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={"address": TOGRILL_SERVICE_INFO.address},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        "address": TOGRILL_SERVICE_INFO.address,
        "model": "Pro-05",
        "probe_count": 0,
        "has_ambient": False,
    }
    assert result["title"] == "Pro-05"
    assert result["result"].unique_id == TOGRILL_SERVICE_INFO.address


async def test_user_selection_ignored(
    hass: __HAC_KEEP__,
) -> None:
    """Test we can select a device."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=TOGRILL_SERVICE_INFO.address,
        source=config_entries.SOURCE_IGNORE,
    )
    entry.add_to_hass(hass)

    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO)
    await hass.async_block_till_done(wait_background_tasks=True)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={"address": TOGRILL_SERVICE_INFO.address},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == TOGRILL_SERVICE_INFO.address


async def test_failed_connect(
    hass: __HAC_KEEP__,
    mock_client: Mock,
    mock_client_class: Mock,
) -> None:
    """Test failure to connect result."""

    mock_client_class.connect.side_effect = BleakError("Failed to connect")

    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={"address": TOGRILL_SERVICE_INFO.address},
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "failed_to_read_config"


async def test_failed_read(
    hass: __HAC_KEEP__,
    mock_client: Mock,
) -> None:
    """Test failure to read from device."""

    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    mock_client.read.side_effect = BleakError("something went wrong")

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={"address": TOGRILL_SERVICE_INFO.address},
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "failed_to_read_config"


async def test_no_devices(
    hass: __HAC_KEEP__,
) -> None:
    """Test missing device."""

    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO_NO_NAME)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_duplicate_setup(
    hass: __HAC_KEEP__,
    mock_entry: MockConfigEntry,
) -> None:
    """Test we can not setup a device again."""

    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO)
    await hass.async_block_till_done(wait_background_tasks=True)

    await setup_entry(hass, mock_entry, [])

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_bluetooth(
    hass: __HAC_KEEP__,
) -> None:
    """Test bluetooth device discovery."""

    # Inject the service info will trigger the flow to start
    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO)
    await hass.async_block_till_done(wait_background_tasks=True)

    result = next(iter(hass.config_entries.flow.async_progress_by_handler(DOMAIN)))

    assert result["step_id"] == "bluetooth_confirm"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        "address": TOGRILL_SERVICE_INFO.address,
        "model": "Pro-05",
        "probe_count": 0,
        "has_ambient": False,
    }
    assert result["title"] == "Pro-05"
    assert result["result"].unique_id == TOGRILL_SERVICE_INFO.address
