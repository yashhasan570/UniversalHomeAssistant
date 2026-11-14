"""Tests for the Denon RS-232 config flow."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.denon_rs232.config_flow import CONF_MODEL_NAME
from universalassistant.components.denon_rs232.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_DEVICE, CONF_MODEL
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

from . import MOCK_DEVICE, MOCK_MODEL, MOCK_MODEL_SELECTION


@pytest.fixture
def mock_async_setup_entry(mock_receiver: MagicMock) -> Generator[AsyncMock]:
    """Prevent config-entry creation tests from setting up the integration."""

    with patch(
        "universalassistant.components.denon_rs232.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        yield mock_setup_entry


async def test_user_form_creates_entry(
    hass: UniversalAssistant,
    mock_receiver: MagicMock,
    mock_async_setup_entry: AsyncMock,
) -> None:
    """Test successful config flow creates an entry."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    with patch(
        "universalassistant.components.denon_rs232.config_flow.DenonReceiver",
        return_value=mock_receiver,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_DEVICE: MOCK_DEVICE, CONF_MODEL: MOCK_MODEL_SELECTION},
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "AVR-3805"
    assert result["data"] == {
        CONF_DEVICE: MOCK_DEVICE,
        CONF_MODEL: MOCK_MODEL,
        CONF_MODEL_NAME: "AVR-3805",
    }
    mock_async_setup_entry.assert_awaited_once()
    mock_receiver.connect.assert_awaited_once()
    mock_receiver.disconnect.assert_awaited_once()


@pytest.mark.parametrize(
    ("exception", "error"),
    [
        (ValueError("Invalid port"), "cannot_connect"),
        (ConnectionError("No response"), "cannot_connect"),
        (OSError("No such device"), "cannot_connect"),
        (RuntimeError("boom"), "unknown"),
    ],
)
async def test_user_form_error(
    hass: UniversalAssistant,
    exception: Exception,
    error: str,
    mock_receiver: MagicMock,
) -> None:
    """Test the user step reports connection and unexpected errors."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    mock_receiver.connect.side_effect = exception

    with patch(
        "universalassistant.components.denon_rs232.config_flow.DenonReceiver",
        return_value=mock_receiver,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_DEVICE: MOCK_DEVICE, CONF_MODEL: MOCK_MODEL_SELECTION},
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": error}

    mock_receiver.connect.side_effect = None

    with patch(
        "universalassistant.components.denon_rs232.config_flow.DenonReceiver",
        return_value=mock_receiver,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_DEVICE: MOCK_DEVICE, CONF_MODEL: MOCK_MODEL_SELECTION},
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_user_duplicate_port_aborts(hass: UniversalAssistant) -> None:
    """Test we abort if the same port is already configured."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={CONF_DEVICE: MOCK_DEVICE, CONF_MODEL: MOCK_MODEL},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {CONF_DEVICE: MOCK_DEVICE, CONF_MODEL: MOCK_MODEL_SELECTION},
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
