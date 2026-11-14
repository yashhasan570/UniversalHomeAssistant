"""Test the StreamLabs config flow."""

from unittest.mock import AsyncMock, patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.streamlabswater.const import DOMAIN
from universalassistant.const import CONF_API_KEY
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_form(hass: __HAC_KEEP__, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with patch("universalassistant.components.streamlabswater.config_flow.StreamlabsClient"):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_API_KEY: "abc"},
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Streamlabs"
    assert result["data"] == {CONF_API_KEY: "abc"}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_cannot_connect(
    hass: __HAC_KEEP__, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.streamlabswater.config_flow.StreamlabsClient.get_locations",
        return_value={},
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_API_KEY: "abc"},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    with patch("universalassistant.components.streamlabswater.config_flow.StreamlabsClient"):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_API_KEY: "abc"},
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Streamlabs"
    assert result["data"] == {CONF_API_KEY: "abc"}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_unknown(hass: __HAC_KEEP__, mock_setup_entry: AsyncMock) -> None:
    """Test we handle unknown error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.streamlabswater.config_flow.StreamlabsClient.get_locations",
        side_effect=Exception,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_API_KEY: "abc"},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "unknown"}

    with patch("universalassistant.components.streamlabswater.config_flow.StreamlabsClient"):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_API_KEY: "abc"},
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Streamlabs"
    assert result["data"] == {CONF_API_KEY: "abc"}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_entry_already_exists(hass: __HAC_KEEP__) -> None:
    """Test we handle if the entry already exists."""

    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_API_KEY: "abc"},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.streamlabswater.config_flow.StreamlabsClient.get_locations",
        side_effect=Exception,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_API_KEY: "abc"},
        )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
