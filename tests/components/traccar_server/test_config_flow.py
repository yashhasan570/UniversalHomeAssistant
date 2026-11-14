"""Test the Traccar Server config flow."""

from collections.abc import Generator
from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytraccar import TraccarAuthenticationException, TraccarException

from universalassistant import config_entries
from universalassistant.components.traccar_server.const import (
    CONF_CUSTOM_ATTRIBUTES,
    CONF_EVENTS,
    CONF_MAX_ACCURACY,
    CONF_SKIP_ACCURACY_FILTER_FOR,
    DOMAIN,
)
from universalassistant.config_entries import ConfigEntryState
from universalassistant.const import (
    CONF_API_TOKEN,
    CONF_HOST,
    CONF_PORT,
    CONF_SSL,
    CONF_VERIFY_SSL,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_form(
    hass: __HAC_KEEP__,
    mock_traccar_api_client: Generator[AsyncMock],
) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_HOST: "1.1.1.1",
            CONF_API_TOKEN: "test-token",
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "1.1.1.1:8082"
    assert result["data"] == {
        CONF_HOST: "1.1.1.1",
        CONF_PORT: "8082",
        CONF_API_TOKEN: "test-token",
        CONF_SSL: False,
        CONF_VERIFY_SSL: True,
    }
    assert result["result"].state is ConfigEntryState.LOADED


@pytest.mark.parametrize(
    ("side_effect", "error"),
    [
        (TraccarException, "cannot_connect"),
        (Exception, "unknown"),
    ],
)
async def test_form_cannot_connect(
    hass: __HAC_KEEP__,
    side_effect: Exception,
    error: str,
    mock_traccar_api_client: Generator[AsyncMock],
) -> None:
    """Test we handle cannot connect error."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    mock_traccar_api_client.get_server.side_effect = side_effect

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_HOST: "1.1.1.1",
            CONF_API_TOKEN: "test-token",
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": error}

    mock_traccar_api_client.get_server.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_HOST: "1.1.1.1",
            CONF_API_TOKEN: "test-token",
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "1.1.1.1:8082"
    assert result["data"] == {
        CONF_HOST: "1.1.1.1",
        CONF_PORT: "8082",
        CONF_API_TOKEN: "test-token",
        CONF_SSL: False,
        CONF_VERIFY_SSL: True,
    }

    assert result["result"].state is ConfigEntryState.LOADED


async def test_options(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_traccar_api_client: Generator[AsyncMock],
) -> None:
    """Test options flow."""
    mock_config_entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    assert mock_config_entry.options.get(CONF_MAX_ACCURACY) == 5.0

    result = await hass.config_entries.options.async_init(mock_config_entry.entry_id)

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={CONF_MAX_ACCURACY: 2.0},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert mock_config_entry.options == {
        CONF_MAX_ACCURACY: 2.0,
        CONF_EVENTS: [],
        CONF_CUSTOM_ATTRIBUTES: [],
        CONF_SKIP_ACCURACY_FILTER_FOR: [],
    }


async def test_abort_already_configured(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_traccar_api_client: Generator[AsyncMock],
) -> None:
    """Test abort for existing server."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_HOST: "1.1.1.1",
            CONF_PORT: "8082",
            CONF_API_TOKEN: "test-token",
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_reauth_flow(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_traccar_api_client: Generator[AsyncMock],
) -> None:
    """Test reauth flow."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    result = await mock_config_entry.start_reauth_flow(hass)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_API_TOKEN: "new-token",
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"

    # Verify the config entry was updated
    assert mock_config_entry.data[CONF_API_TOKEN] == "new-token"


@pytest.mark.parametrize(
    ("side_effect", "error"),
    [
        (TraccarAuthenticationException, "invalid_auth"),
        (TraccarException, "cannot_connect"),
        (Exception, "unknown"),
    ],
)
async def test_reauth_flow_errors(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_traccar_api_client: Generator[AsyncMock],
    side_effect: Exception,
    error: str,
) -> None:
    """Test reauth flow with errors."""
    mock_config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_config_entry.entry_id)

    result = await mock_config_entry.start_reauth_flow(hass)

    mock_traccar_api_client.get_server.side_effect = side_effect

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_API_TOKEN: "new-token",
        },
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": error}

    # Test recovery after error
    mock_traccar_api_client.get_server.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_API_TOKEN: "new-token",
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
