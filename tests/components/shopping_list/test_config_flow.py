"""Test config flow."""

from universalassistant.components.shopping_list.const import DOMAIN
from universalassistant.config_entries import SOURCE_IMPORT, SOURCE_USER
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType


async def test_import(hass: UniversalAssistant) -> None:
    """Test entry will be imported."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_IMPORT}, data={}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == DOMAIN


async def test_user(hass: UniversalAssistant) -> None:
    """Test we can start a config flow."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


async def test_user_confirm(hass: UniversalAssistant) -> None:
    """Test we can finish a config flow."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["result"].data == {}
    assert result["result"].unique_id == DOMAIN


async def test_onboarding_flow(hass: UniversalAssistant) -> None:
    """Test the onboarding configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": "onboarding"}
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Shopping list"
    assert result["data"] == {}
    assert result["result"].unique_id == DOMAIN
