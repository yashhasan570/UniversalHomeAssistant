"""Test the NASweb config flow."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from webio_api.api_client import AuthError

from universalassistant import config_entries
from universalassistant.components.nasweb.const import DOMAIN
from universalassistant.config_entries import ConfigFlowResult
from universalassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.helpers.network import NoURLAvailableError

from .conftest import (
    BASE_CONFIG_FLOW,
    BASE_COORDINATOR,
    BASE_NASWEB_DATA,
    TEST_SERIAL_NUMBER,
)

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


TEST_USER_INPUT = {
    CONF_HOST: "1.1.1.1",
    CONF_USERNAME: "test-username",
    CONF_PASSWORD: "test-password",
}


async def _add_test_config_entry(hass: __HAC_KEEP__) -> ConfigFlowResult:
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result.get("type") is FlowResultType.FORM
    assert not result.get("errors")

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )
    await hass.async_block_till_done()
    return result2


async def test_form(
    hass: __HAC_KEEP__,
    mock_setup_entry: AsyncMock,
    validate_input_all_ok: dict[str, AsyncMock | MagicMock],
) -> None:
    """Test the form."""
    result = await _add_test_config_entry(hass)

    assert result.get("type") is FlowResultType.CREATE_ENTRY
    assert result.get("title") == "1.1.1.1"
    assert result.get("data") == TEST_USER_INPUT

    config_entry = result.get("result")
    assert config_entry is not None
    assert config_entry.unique_id == TEST_SERIAL_NUMBER
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.usefixtures("validate_input_all_ok")
async def test_form_cannot_connect(hass: __HAC_KEEP__) -> None:
    """Test cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(BASE_CONFIG_FLOW + "WebioAPI.check_connection", return_value=False):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_USER_INPUT
        )

    assert result2.get("type") is FlowResultType.FORM
    assert result2.get("errors") == {"base": "cannot_connect"}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )

    assert result2.get("type") is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("validate_input_all_ok")
async def test_form_invalid_auth(hass: __HAC_KEEP__) -> None:
    """Test invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        BASE_CONFIG_FLOW + "WebioAPI.refresh_device_info",
        side_effect=AuthError,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_USER_INPUT
        )

    assert result2.get("type") is FlowResultType.FORM
    assert result2.get("errors") == {"base": "invalid_auth"}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )

    assert result2.get("type") is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("validate_input_all_ok")
async def test_form_missing_internal_url(hass: __HAC_KEEP__) -> None:
    """Test missing internal url."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        BASE_NASWEB_DATA + "NASwebData.get_webhook_url", side_effect=NoURLAvailableError
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_USER_INPUT
        )
        assert result2.get("type") is FlowResultType.FORM
        assert result2.get("errors") == {"base": "missing_internal_url"}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )

    assert result2.get("type") is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("validate_input_all_ok")
async def test_form_missing_nasweb_data(hass: __HAC_KEEP__) -> None:
    """Test invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        BASE_CONFIG_FLOW + "WebioAPI.get_serial_number",
        return_value=None,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_USER_INPUT
        )
        assert result2.get("type") is FlowResultType.FORM
        assert result2.get("errors") == {"base": "missing_nasweb_data"}
    with patch(BASE_CONFIG_FLOW + "WebioAPI.status_subscription", return_value=False):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_USER_INPUT
        )
        assert result2.get("type") is FlowResultType.FORM
        assert result2.get("errors") == {"base": "missing_nasweb_data"}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )

    assert result2.get("type") is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("validate_input_all_ok")
async def test_missing_status(hass: __HAC_KEEP__) -> None:
    """Test missing status update."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        BASE_COORDINATOR + "NotificationCoordinator.check_connection",
        return_value=False,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_USER_INPUT
        )
        assert result2.get("type") is FlowResultType.FORM
        assert result2.get("errors") == {"base": "missing_status"}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )

    assert result2.get("type") is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("validate_input_all_ok")
async def test_form_exception(hass: __HAC_KEEP__) -> None:
    """Test other exceptions."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.nasweb.config_flow.validate_input",
        side_effect=Exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], TEST_USER_INPUT
        )
        assert result2.get("type") is FlowResultType.FORM
        assert result2.get("errors") == {"base": "unknown"}

    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )

    assert result2.get("type") is FlowResultType.CREATE_ENTRY


async def test_form_already_configured(
    hass: __HAC_KEEP__,
    validate_input_all_ok: dict[str, AsyncMock | MagicMock],
) -> None:
    """Test already configured device."""
    result = await _add_test_config_entry(hass)
    config_entry = result.get("result")
    assert config_entry is not None
    assert config_entry.unique_id == TEST_SERIAL_NUMBER

    result2_1 = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result2_2 = await hass.config_entries.flow.async_configure(
        result2_1["flow_id"], TEST_USER_INPUT
    )
    await hass.async_block_till_done()

    assert result2_2.get("type") is FlowResultType.ABORT
    assert result2_2.get("reason") == "already_configured"
