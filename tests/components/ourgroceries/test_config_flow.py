"""Test the OurGroceries config flow."""

from unittest.mock import AsyncMock, patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.ourgroceries.config_flow import (
    ClientError,
    InvalidLoginException,
)
from universalassistant.components.ourgroceries.const import DOMAIN
from universalassistant.const import CONF_PASSWORD, CONF_USERNAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_form(hass: __HAC_KEEP__, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}

    with patch(
        "universalassistant.components.ourgroceries.config_flow.OurGroceries.login",
        return_value=True,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "test-username"
    assert result2["data"] == {
        "username": "test-username",
        "password": "test-password",
    }
    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.parametrize(
    ("exception", "error"),
    [
        (InvalidLoginException, "invalid_auth"),
        (ClientError, "cannot_connect"),
        (TimeoutError, "cannot_connect"),
        (Exception, "unknown"),
    ],
)
async def test_form_error(
    hass: __HAC_KEEP__, exception: Exception, error: str, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle form errors."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.ourgroceries.config_flow.OurGroceries.login",
        side_effect=exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": error}
    with patch(
        "universalassistant.components.ourgroceries.config_flow.OurGroceries.login",
        return_value=True,
    ):
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["title"] == "test-username"
    assert result3["data"] == {
        "username": "test-username",
        "password": "test-password",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_reauth(
    hass: __HAC_KEEP__,
    ourgroceries_config_entry: MockConfigEntry,
    mock_setup_entry: AsyncMock,
) -> None:
    """Test reauth updates the password."""
    ourgroceries_config_entry.add_to_hass(hass)

    result = await ourgroceries_config_entry.start_reauth_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"

    with patch(
        "universalassistant.components.ourgroceries.config_flow.OurGroceries"
    ) as mock_og:
        mock_og.return_value.login = AsyncMock(return_value=True)
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_PASSWORD: "new-password"}
        )
        await hass.async_block_till_done()

    mock_og.assert_called_once_with(
        ourgroceries_config_entry.data[CONF_USERNAME], "new-password"
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert ourgroceries_config_entry.data[CONF_PASSWORD] == "new-password"


@pytest.mark.parametrize(
    ("exception", "error"),
    [
        (InvalidLoginException, "invalid_auth"),
        (ClientError, "cannot_connect"),
        (TimeoutError, "cannot_connect"),
        (Exception, "unknown"),
    ],
)
async def test_reauth_errors(
    hass: __HAC_KEEP__,
    ourgroceries_config_entry: MockConfigEntry,
    mock_setup_entry: AsyncMock,
    exception: Exception,
    error: str,
) -> None:
    """Test reauth handles errors and can recover."""
    ourgroceries_config_entry.add_to_hass(hass)

    result = await ourgroceries_config_entry.start_reauth_flow(hass)

    with patch(
        "universalassistant.components.ourgroceries.config_flow.OurGroceries.login",
        side_effect=exception,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_PASSWORD: "wrong-password"}
        )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "reauth_confirm"
    assert result["errors"] == {"base": error}

    with patch(
        "universalassistant.components.ourgroceries.config_flow.OurGroceries.login",
        return_value=True,
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_PASSWORD: "new-password"}
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "reauth_successful"
    assert ourgroceries_config_entry.data[CONF_PASSWORD] == "new-password"
