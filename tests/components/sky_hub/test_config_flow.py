"""Tests for Sky Hub config flows."""

from unittest.mock import MagicMock

from aiohttp import ClientError, ClientPayloadError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.sky_hub.const import DEFAULT_HOST, DOMAIN
from universalassistant.config_entries import SOURCE_IMPORT, SOURCE_USER
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

CONNECT_ERRORS = [
    pytest.param(False, None, id="unsuccessful_init"),
    pytest.param(True, ClientPayloadError("Incomplete response"), id="payload_error"),
]


@pytest.mark.usefixtures("mock_setup_entry", "mock_router")
async def test_successful_user_config_flow(hass: UniversalAssistant) -> None:
    """Test a successful user config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_HOST: DEFAULT_HOST}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == DEFAULT_HOST
    assert result["data"] == {CONF_HOST: DEFAULT_HOST}


@pytest.mark.usefixtures("mock_setup_entry")
@pytest.mark.parametrize(("connected", "connect_error"), CONNECT_ERRORS)
async def test_user_cannot_connect_and_retry(
    hass: UniversalAssistant,
    mock_router: MagicMock,
    connected: bool,
    connect_error: ClientError | None,
) -> None:
    """Test connection failures show errors and the user can retry successfully."""
    mock_router.success_init = connected
    mock_router.async_connect.side_effect = connect_error

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_HOST: DEFAULT_HOST}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "cannot_connect"}

    mock_router.success_init = True
    mock_router.async_connect.reset_mock()
    mock_router.async_connect.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_HOST: DEFAULT_HOST}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == DEFAULT_HOST
    assert result["data"] == {CONF_HOST: DEFAULT_HOST}


@pytest.mark.usefixtures("mock_setup_entry", "mock_router")
async def test_import_creates_entry(hass: UniversalAssistant) -> None:
    """Test a successful YAML import."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_IMPORT}, data={CONF_HOST: DEFAULT_HOST}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == DEFAULT_HOST
    assert result["data"] == {CONF_HOST: DEFAULT_HOST}


@pytest.mark.parametrize(("connected", "connect_error"), CONNECT_ERRORS)
async def test_import_cannot_connect(
    hass: UniversalAssistant,
    mock_router: MagicMock,
    connected: bool,
    connect_error: ClientError | None,
) -> None:
    """Test failed YAML imports do not create entries."""
    mock_router.success_init = connected
    mock_router.async_connect.side_effect = connect_error

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_IMPORT}, data={CONF_HOST: DEFAULT_HOST}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "cannot_connect"
    assert not hass.config_entries.async_entries(DOMAIN)


@pytest.mark.parametrize("source", [SOURCE_USER, SOURCE_IMPORT])
async def test_already_configured(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    source: str,
) -> None:
    """Test config aborts when the host is already configured."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": source}, data={CONF_HOST: DEFAULT_HOST}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


@pytest.mark.usefixtures("mock_setup_entry", "mock_router")
@pytest.mark.parametrize("source", [SOURCE_USER, SOURCE_IMPORT])
async def test_different_host(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    source: str,
) -> None:
    """Test config allows adding a different host."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": source}, data={CONF_HOST: "192.168.0.1"}
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "192.168.0.1"
    assert result["data"] == {CONF_HOST: "192.168.0.1"}
    assert len(hass.config_entries.async_entries(DOMAIN)) == 2
