"""Define tests for the IQVIA config flow."""

from typing import Any

import pytest

from universalassistant.components.iqvia.const import CONF_ZIP_CODE, DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType


@pytest.mark.usefixtures("config_entry")
async def test_duplicate_error(hass: UniversalAssistant, config: dict[str, Any]) -> None:
    """Test that errors are shown when duplicates are added."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=config
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


@pytest.mark.usefixtures("setup_iqvia")
async def test_invalid_zip_code(hass: UniversalAssistant) -> None:
    """Test that an invalid ZIP code key throws an error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_ZIP_CODE: "bad"}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {CONF_ZIP_CODE: "invalid_zip_code"}

    # recover
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_ZIP_CODE: "12345"}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "12345"
    assert result["data"] == {CONF_ZIP_CODE: "12345"}


async def test_show_form(hass: UniversalAssistant) -> None:
    """Test that the form is served with no input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


@pytest.mark.usefixtures("setup_iqvia")
async def test_step_user(hass: UniversalAssistant, config: dict[str, Any]) -> None:
    """Test that the user step works (without MFA)."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert not result["errors"]

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=config
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "12345"
    assert result["data"] == {CONF_ZIP_CODE: "12345"}
    assert result["result"].unique_id == "12345"
