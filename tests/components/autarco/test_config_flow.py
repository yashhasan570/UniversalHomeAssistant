"""Test the Autarco config flow."""

from unittest.mock import AsyncMock, patch

from autarco import AutarcoAuthenticationError, AutarcoConnectionError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.autarco.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_EMAIL, CONF_PASSWORD
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_full_user_flow(
    hass: __HAC_KEEP__,
    mock_autarco_client: AsyncMock,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test the full user configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result.get("type") is FlowResultType.FORM
    assert result.get("step_id") == "user"
    assert not result.get("errors")

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_EMAIL: "test@autarco.com", CONF_PASSWORD: "test-password"},
    )

    assert result.get("type") is FlowResultType.CREATE_ENTRY
    assert result.get("title") == "test@autarco.com"
    assert result.get("data") == {
        CONF_EMAIL: "test@autarco.com",
        CONF_PASSWORD: "test-password",
    }
    assert len(mock_autarco_client.get_account.mock_calls) == 1
    assert len(mock_setup_entry.mock_calls) == 1


async def test_duplicate_entry(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_autarco_client: AsyncMock,
) -> None:
    """Test abort when setting up duplicate entry."""
    mock_config_entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result.get("type") is FlowResultType.FORM
    assert not result.get("errors")

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_EMAIL: "test@autarco.com", CONF_PASSWORD: "test-password"},
    )

    assert result.get("type") is FlowResultType.ABORT
    assert result.get("reason") == "already_configured"


@pytest.mark.parametrize(
    ("exception", "error"),
    [
        (AutarcoConnectionError, "cannot_connect"),
        (AutarcoAuthenticationError, "invalid_auth"),
    ],
)
@pytest.mark.usefixtures("mock_setup_entry")
async def test_exceptions(
    hass: __HAC_KEEP__,
    mock_autarco_client: AsyncMock,
    exception: Exception,
    error: str,
) -> None:
    """Test exceptions."""
    mock_autarco_client.get_account.side_effect = exception
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_EMAIL: "test@autarco.com", CONF_PASSWORD: "test-password"},
    )
    assert result.get("type") is FlowResultType.FORM
    assert result.get("errors") == {"base": error}

    # Recover from error
    mock_autarco_client.get_account.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_EMAIL: "test@autarco.com", CONF_PASSWORD: "test-password"},
    )
    assert result.get("type") is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("mock_setup_entry")
async def test_step_reauth(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test reauth flow."""
    mock_config_entry.add_to_hass(hass)
    result = await mock_config_entry.start_reauth_flow(hass)

    assert result.get("type") is FlowResultType.FORM
    assert result.get("step_id") == "reauth_confirm"

    with patch("universalassistant.components.autarco.config_flow.Autarco", autospec=True):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input={CONF_PASSWORD: "new-password"},
        )

    assert result.get("type") is FlowResultType.ABORT
    assert result.get("reason") == "reauth_successful"

    assert len(hass.config_entries.async_entries()) == 1
    assert mock_config_entry.data[CONF_PASSWORD] == "new-password"


@pytest.mark.parametrize(
    ("exception", "error"),
    [
        (AutarcoConnectionError, "cannot_connect"),
        (AutarcoAuthenticationError, "invalid_auth"),
    ],
)
@pytest.mark.usefixtures("mock_setup_entry")
async def test_step_reauth_exceptions(
    hass: __HAC_KEEP__,
    mock_autarco_client: AsyncMock,
    mock_config_entry: MockConfigEntry,
    exception: Exception,
    error: str,
) -> None:
    """Test exceptions in reauth flow."""
    mock_autarco_client.get_account.side_effect = exception
    mock_config_entry.add_to_hass(hass)
    result = await mock_config_entry.start_reauth_flow(hass)

    assert result.get("type") is FlowResultType.FORM
    assert result.get("step_id") == "reauth_confirm"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_PASSWORD: "new-password"},
    )
    assert result.get("type") is FlowResultType.FORM
    assert result.get("errors") == {"base": error}

    # Recover from error
    mock_autarco_client.get_account.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_PASSWORD: "new-password"},
    )
    assert result.get("type") is FlowResultType.ABORT
    assert result.get("reason") == "reauth_successful"

    assert len(hass.config_entries.async_entries()) == 1
    assert mock_config_entry.data[CONF_PASSWORD] == "new-password"
