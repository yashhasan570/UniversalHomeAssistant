"""Test the Wolf SmartSet Service config flow."""

from unittest.mock import patch

from httpx2 import RequestError
import pytest
from pytest_universalassistant.common import MockConfigEntry
from wolf_comm.models import Device
from wolf_comm.token_auth import InvalidAuth

from universalassistant import config_entries
from universalassistant.components.wolflink.const import DOMAIN
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from .const import CONFIG

INPUT_CONFIG = {
    CONF_USERNAME: CONFIG[CONF_USERNAME],
    CONF_PASSWORD: CONFIG[CONF_PASSWORD],
}

DEVICE = Device(1234, 5678, "test-device")
SECOND_DEVICE = Device(5678, 9999, "second-device")


async def _start_user_flow(hass: __HAC_KEEP__) -> dict:
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"
    return result


async def test_show_form(hass: __HAC_KEEP__) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


async def test_create_entry(hass: __HAC_KEEP__) -> None:
    """Test entry creation only stores credentials, not the device list."""
    result = await _start_user_flow(hass)

    with (
        patch(
            "universalassistant.components.wolflink.config_flow.WolfClient.fetch_system_list",
            return_value=[DEVICE, SECOND_DEVICE],
        ),
        patch("universalassistant.components.wolflink.async_setup_entry", return_value=None),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=INPUT_CONFIG
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == CONFIG[CONF_USERNAME]
    assert result["data"] == CONFIG
    assert result["result"].unique_id == CONFIG[CONF_USERNAME].lower()


@pytest.mark.parametrize(
    ("side_effect", "expected_error"),
    [
        pytest.param(InvalidAuth, "invalid_auth", id="invalid_auth"),
        pytest.param(RequestError("boom"), "cannot_connect", id="cannot_connect"),
        pytest.param(Exception("boom"), "unknown", id="unknown"),
    ],
)
async def test_user_flow_errors(
    hass: __HAC_KEEP__, side_effect: Exception, expected_error: str
) -> None:
    """Test error handling in the user step keeps the form open with errors."""
    result = await _start_user_flow(hass)

    with patch(
        "universalassistant.components.wolflink.config_flow.WolfClient.fetch_system_list",
        side_effect=side_effect,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=INPUT_CONFIG
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": expected_error}

    with (
        patch(
            "universalassistant.components.wolflink.config_flow.WolfClient.fetch_system_list",
            return_value=[DEVICE],
        ),
        patch("universalassistant.components.wolflink.async_setup_entry", return_value=None),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=INPUT_CONFIG
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_no_devices_abort(hass: __HAC_KEEP__) -> None:
    """Test we abort if the account has no devices."""
    result = await _start_user_flow(hass)

    with patch(
        "universalassistant.components.wolflink.config_flow.WolfClient.fetch_system_list",
        return_value=[],
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=INPUT_CONFIG
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_devices"


async def test_already_configured_aborts(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test entries with the same username can't be configured twice."""
    mock_config_entry.add_to_hass(hass)

    result = await _start_user_flow(hass)

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=INPUT_CONFIG
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
