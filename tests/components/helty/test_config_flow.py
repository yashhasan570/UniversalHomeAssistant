"""Test the Helty Flow config flow."""

from unittest.mock import AsyncMock

from pyhelty import HeltyConnectionError, HeltyError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.helty.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_HOST
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from .conftest import DEVICE_NAME, HOST

USER_INPUT = {CONF_HOST: HOST}


async def test_user_flow(
    hass: __HAC_KEEP__,
    mock_helty_client: AsyncMock,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test the happy path of the user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], USER_INPUT
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == DEVICE_NAME
    assert result["data"] == USER_INPUT
    assert len(mock_setup_entry.mock_calls) == 1


async def test_user_flow_empty_name(
    hass: __HAC_KEEP__,
    mock_helty_client: AsyncMock,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test the host is used as the title when the unit reports no name."""
    mock_helty_client.async_get_name.return_value = ""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], USER_INPUT
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == HOST


@pytest.mark.parametrize(
    ("side_effect", "error"),
    [
        (HeltyConnectionError, "cannot_connect"),
        (HeltyError, "unknown"),
    ],
)
async def test_user_flow_errors(
    hass: __HAC_KEEP__,
    mock_helty_client: AsyncMock,
    mock_setup_entry: AsyncMock,
    side_effect: type[Exception],
    error: str,
) -> None:
    """Test errors are shown, then the flow recovers."""
    mock_helty_client.async_get_name.side_effect = side_effect

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], USER_INPUT
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": error}

    mock_helty_client.async_get_name.side_effect = None
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], USER_INPUT
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_already_configured(
    hass: __HAC_KEEP__,
    mock_helty_client: AsyncMock,
    mock_setup_entry: AsyncMock,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test we abort if a unit at the same host is already configured."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], USER_INPUT
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
