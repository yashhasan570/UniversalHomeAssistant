"""Test the AirPatrol config flow."""

from unittest.mock import patch

from airpatrol.api import AirPatrolAPI, AirPatrolAuthenticationError, AirPatrolError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.airpatrol.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_ACCESS_TOKEN, CONF_EMAIL, CONF_PASSWORD
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

TEST_USER_INPUT = {
    CONF_EMAIL: "test@example.com",
    CONF_PASSWORD: "test_password",
}


async def test_user_flow_success(
    hass: UniversalAssistant,
    get_client: AirPatrolAPI,
) -> None:
    """Test successful user flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=TEST_USER_INPUT
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == TEST_USER_INPUT[CONF_EMAIL]
    assert result["data"] == {
        **TEST_USER_INPUT,
        CONF_ACCESS_TOKEN: "test_access_token",
    }
    assert result["result"].unique_id == "test_user_id"


async def test_async_step_reauth_confirm_success(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry, get_client: AirPatrolAPI
) -> None:
    """Test successful reauthentication via async_step_reauth_confirm."""
    mock_config_entry.add_to_hass(hass)
    result = await mock_config_entry.start_reauth_flow(hass)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=TEST_USER_INPUT
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"

    assert mock_config_entry.data[CONF_PASSWORD] == "test_password"
    assert mock_config_entry.data[CONF_ACCESS_TOKEN] == "test_access_token"


async def test_async_step_reauth_confirm_invalid_auth(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
    get_client: AirPatrolAPI,
) -> None:
    """Test reauthentication failure due to invalid credentials."""
    mock_config_entry.add_to_hass(hass)
    result = await mock_config_entry.start_reauth_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    with patch(
        "universalassistant.components.airpatrol.config_flow.AirPatrolAPI.authenticate",
        side_effect=AirPatrolAuthenticationError("fail"),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=TEST_USER_INPUT
        )
        assert result["type"] is FlowResultType.FORM
        assert result["step_id"] == "reauth_confirm"
        assert result["errors"] == {"base": "invalid_auth"}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input=TEST_USER_INPUT,
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert mock_config_entry.data[CONF_PASSWORD] == "test_password"
    assert mock_config_entry.data[CONF_ACCESS_TOKEN] == "test_access_token"


async def test_async_step_reauth_confirm_another_account_failure(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry, get_client: AirPatrolAPI
) -> None:
    """Test reauthentication failure due to another account."""
    mock_config_entry.add_to_hass(hass)
    result = await mock_config_entry.start_reauth_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    get_client.get_unique_id.return_value = "different_user_id"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_EMAIL: "test2@example.com", CONF_PASSWORD: "test_password2"},
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "unique_id_mismatch"


@pytest.mark.parametrize(
    ("side_effect", "expected_error"),
    [
        (AirPatrolError("fail"), "cannot_connect"),
        (AirPatrolAuthenticationError("fail"), "invalid_auth"),
    ],
)
async def test_user_flow_error(
    hass: UniversalAssistant,
    side_effect,
    expected_error,
    get_client: AirPatrolAPI,
) -> None:
    """Test user flow with invalid authentication."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "universalassistant.components.airpatrol.config_flow.AirPatrolAPI.authenticate",
        side_effect=side_effect,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input=TEST_USER_INPUT
        )

        assert result["type"] is FlowResultType.FORM
        assert result["errors"] == {"base": expected_error}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=TEST_USER_INPUT
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == TEST_USER_INPUT[CONF_EMAIL]
    assert result["data"] == {
        **TEST_USER_INPUT,
        CONF_ACCESS_TOKEN: "test_access_token",
    }
    assert result["result"].unique_id == "test_user_id"


async def test_user_flow_already_configured(
    hass: UniversalAssistant,
    get_client: AirPatrolAPI,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test user flow when already configured."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=TEST_USER_INPUT
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
