"""Tests for the config flow."""

from universalassistant.components.dsmr_reader.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType


async def test_user_step(hass: UniversalAssistant) -> None:
    """Test the user step call."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "confirm"
    assert result["errors"] is None

    config_result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={}
    )

    assert config_result["type"] is FlowResultType.CREATE_ENTRY
    assert config_result["title"] == "DSMR Reader"

    duplicate_result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert duplicate_result["type"] is FlowResultType.ABORT
    assert duplicate_result["reason"] == "single_instance_allowed"
