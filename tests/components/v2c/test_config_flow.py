"""Test the V2C config flow."""

from unittest.mock import AsyncMock

import pytest
from pytrydan.exceptions import TrydanError

from universalassistant.components.v2c.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_full_flow(
    hass: __HAC_KEEP__, mock_setup_entry: AsyncMock, mock_v2c_client: AsyncMock
) -> None:
    """Test we can finish a config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_HOST: "1.1.1.1"},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "EVSE 1.1.1.1"
    assert result["data"] == {CONF_HOST: "1.1.1.1"}
    assert result["result"].unique_id == "ABC123"
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.parametrize(
    ("side_effect", "error"),
    [
        (TrydanError, "cannot_connect"),
        (Exception, "unknown"),
    ],
)
@pytest.mark.usefixtures("mock_setup_entry")
async def test_form_cannot_connect(
    hass: __HAC_KEEP__, side_effect: Exception, error: str, mock_v2c_client: AsyncMock
) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    mock_v2c_client.get_data.side_effect = side_effect
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_HOST: "1.1.1.1"},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": error}
    mock_v2c_client.get_data.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_HOST: "1.1.1.1"},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "EVSE 1.1.1.1"
    assert result["data"] == {CONF_HOST: "1.1.1.1"}
