"""Test the Namecheap DynamicDNS config flow."""

from unittest.mock import AsyncMock

from aiohttp import ClientError
import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.namecheapdns.const import DOMAIN, UPDATE_URL
from universalassistant.components.namecheapdns.helpers import AuthFailed
from universalassistant.config_entries import SOURCE_REAUTH, SOURCE_USER, ConfigEntryState
from universalassistant.const import CONF_PASSWORD
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

from .conftest import TEST_USER_INPUT


@pytest.mark.usefixtures("mock_namecheap")
async def test_form(hass: UniversalAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "home.example.com"
    assert result["data"] == TEST_USER_INPUT

    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.parametrize(
    ("side_effect", "text_error"),
    [
        (ValueError, "unknown"),
        (False, "update_failed"),
        (ClientError, "cannot_connect"),
    ],
)
async def test_form_errors(
    hass: UniversalAssistant,
    mock_setup_entry: AsyncMock,
    mock_namecheap: AsyncMock,
    side_effect: Exception | bool,
    text_error: str,
) -> None:
    """Test we handle errors."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    mock_namecheap.side_effect = [side_effect]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": text_error}

    mock_namecheap.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], TEST_USER_INPUT
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "home.example.com"
    assert result["data"] == TEST_USER_INPUT
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.usefixtures("mock_namecheap")
async def test_reconfigure(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
) -> None:
    """Test reconfigure flow."""
    config_entry.add_to_hass(hass)
    result = await config_entry.start_reconfigure_flow(hass)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_PASSWORD: "new-password"}
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"
    assert config_entry.data[CONF_PASSWORD] == "new-password"


@pytest.mark.parametrize(
    ("side_effect", "text_error"),
    [
        (ValueError, "unknown"),
        (False, "update_failed"),
        (ClientError, "cannot_connect"),
        (AuthFailed, "invalid_auth"),
    ],
)
async def test_reconfigure_errors(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    mock_namecheap: AsyncMock,
    side_effect: Exception | bool,
    text_error: str,
) -> None:
    """Test we handle errors."""

    config_entry.add_to_hass(hass)
    result = await config_entry.start_reconfigure_flow(hass)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reconfigure"

    mock_namecheap.side_effect = [side_effect]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_PASSWORD: "new-password"}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": text_error}

    mock_namecheap.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_PASSWORD: "new-password"}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reconfigure_successful"

    assert config_entry.data[CONF_PASSWORD] == "new-password"


@pytest.mark.usefixtures("mock_namecheap")
async def test_reauth(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test reauth flow."""
    aioclient_mock.get(
        UPDATE_URL,
        params=TEST_USER_INPUT,
        text="<interface-response><ErrCount>0</ErrCount></interface-response>",
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    result = await config_entry.start_reauth_flow(hass)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_PASSWORD: "new-password"}
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert config_entry.data[CONF_PASSWORD] == "new-password"


@pytest.mark.parametrize(
    ("side_effect", "text_error"),
    [
        (ValueError, "unknown"),
        (False, "update_failed"),
        (ClientError, "cannot_connect"),
        (AuthFailed, "invalid_auth"),
    ],
)
async def test_reauth_errors(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    mock_namecheap: AsyncMock,
    side_effect: Exception | bool,
    text_error: str,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test we handle errors."""
    aioclient_mock.get(
        UPDATE_URL,
        params=TEST_USER_INPUT,
        text="<interface-response><ErrCount>0</ErrCount></interface-response>",
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.LOADED

    result = await config_entry.start_reauth_flow(hass)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    mock_namecheap.side_effect = [side_effect]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_PASSWORD: "new-password"}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": text_error}

    mock_namecheap.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_PASSWORD: "new-password"}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"

    assert config_entry.data[CONF_PASSWORD] == "new-password"


async def test_initiate_reauth_flow(
    hass: UniversalAssistant,
    config_entry: MockConfigEntry,
    aioclient_mock: AiohttpClientMocker,
) -> None:
    """Test authentication error initiates reauth flow."""

    aioclient_mock.get(
        UPDATE_URL,
        params=TEST_USER_INPUT,
        text=(
            "<interface-response><ErrCount>1</ErrCount><errors>"
            "<Err1>Passwords do not match</Err1>"
            "</errors></interface-response>"
        ),
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    assert config_entry.state is ConfigEntryState.SETUP_ERROR

    flows = hass.config_entries.flow.async_progress()
    assert len(flows) == 1

    flow = flows[0]
    assert flow.get("step_id") == "reauth_confirm"
    assert flow.get("handler") == DOMAIN

    assert "context" in flow
    assert flow["context"].get("source") == SOURCE_REAUTH
    assert flow["context"].get("entry_id") == config_entry.entry_id
