"""Test Dremel 3D Printer config flow."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry
from requests.exceptions import ConnectTimeout

from universalassistant.components.dremel_3d_printer.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_SOURCE
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from .conftest import CONF_DATA, patch_async_setup_entry

MOCK = "universalassistant.components.dremel_3d_printer.config_flow.Dremel3DPrinter"


async def test_full_user_flow_implementation(hass: __HAC_KEEP__, connection) -> None:
    """Test the full manual user flow from start to finish."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={CONF_SOURCE: SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch_async_setup_entry():
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=CONF_DATA
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "DREMEL 3D45"
    assert result["data"] == CONF_DATA
    assert result["result"].unique_id == "123456789"


async def test_already_configured(
    hass: __HAC_KEEP__, connection, config_entry: MockConfigEntry
) -> None:
    """Test we abort if the device is already configured."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={CONF_SOURCE: SOURCE_USER}, data=CONF_DATA
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_cannot_connect(hass: __HAC_KEEP__, connection) -> None:
    """Test we show user form on connection error."""
    with patch(MOCK, side_effect=ConnectTimeout):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={CONF_SOURCE: SOURCE_USER}, data=CONF_DATA
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "cannot_connect"}

    with patch_async_setup_entry():
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=CONF_DATA
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == CONF_DATA


async def test_unknown_error(hass: __HAC_KEEP__, connection) -> None:
    """Test we show user form on unknown error."""
    with patch(MOCK, side_effect=Exception):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={CONF_SOURCE: SOURCE_USER}, data=CONF_DATA
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "unknown"}

    with patch_async_setup_entry():
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=CONF_DATA
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "DREMEL 3D45"
    assert result["data"] == CONF_DATA
