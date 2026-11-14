"""Tests for the Hase iQ config flow."""

from unittest.mock import AsyncMock, MagicMock

from pyhaseiq import ConnectionFailedError, ProtocolError, ResponseTimeoutError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.hase_iq.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_HOST
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

from .conftest import MOCK_HOST


@pytest.mark.usefixtures("mock_client")
async def test_user_flow(hass: UniversalAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test configuring a stove by its address."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_HOST: MOCK_HOST}
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Hase iQ"
    assert result["data"] == {CONF_HOST: MOCK_HOST}
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.usefixtures("mock_setup_entry")
@pytest.mark.parametrize(
    ("exception", "error"),
    [
        pytest.param(
            ConnectionFailedError("unreachable"), "cannot_connect", id="unreachable"
        ),
        pytest.param(ResponseTimeoutError("silent"), "cannot_connect", id="silent"),
        pytest.param(ProtocolError("garbled"), "cannot_connect", id="garbled"),
        pytest.param(RuntimeError("boom"), "unknown", id="unexpected"),
    ],
)
async def test_user_flow_errors(
    hass: UniversalAssistant,
    mock_client: MagicMock,
    exception: Exception,
    error: str,
) -> None:
    """Test the user flow reports a stove it cannot read, and recovers."""
    mock_client.get_phase.side_effect = exception

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_HOST: MOCK_HOST}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": error}

    mock_client.get_phase.side_effect = None
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_HOST: MOCK_HOST}
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("mock_client")
async def test_already_configured(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test a stove already configured at the same address is refused."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_HOST: MOCK_HOST}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
