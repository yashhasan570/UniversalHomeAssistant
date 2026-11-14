"""Test the Aurora config flow."""

from unittest.mock import AsyncMock

from aiohttp import ClientError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.aurora.const import CONF_THRESHOLD, DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_LATITUDE, CONF_LOCATION, CONF_LONGITUDE
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from . import setup_integration

DATA = {
    CONF_LATITUDE: -10,
    CONF_LONGITUDE: 10.2,
}

USER_INPUT = {CONF_LOCATION: DATA}


async def test_full_flow(
    hass: __HAC_KEEP__, mock_setup_entry: AsyncMock, mock_aurora_client: AsyncMock
) -> None:
    """Test full flow."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=USER_INPUT
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Aurora visibility"
    assert result["data"] == DATA
    assert result["result"].unique_id == "10.2_-10.0"
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.parametrize(
    ("side_effect", "error"),
    [
        (ClientError, "cannot_connect"),
        (Exception, "unknown"),
    ],
)
@pytest.mark.usefixtures("mock_setup_entry")
async def test_form_errors(
    hass: __HAC_KEEP__,
    mock_aurora_client: AsyncMock,
    side_effect: Exception,
    error: str,
) -> None:
    """Test if invalid response or no connection returned from the API."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    mock_aurora_client.get_forecast_data.side_effect = side_effect

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=USER_INPUT
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": error}

    mock_aurora_client.get_forecast_data.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=USER_INPUT
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("mock_setup_entry")
async def test_option_flow(
    hass: __HAC_KEEP__,
    mock_aurora_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test option flow."""
    await setup_integration(hass, mock_config_entry)

    result = await hass.config_entries.options.async_init(mock_config_entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={CONF_THRESHOLD: 65},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"][CONF_THRESHOLD] == 65
