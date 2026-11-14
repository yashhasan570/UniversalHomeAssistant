"""Test the LaCrosse View config flow."""

from unittest.mock import AsyncMock, patch

from lacrosse_view import Location, LoginError
import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.lacrosse_view.const import DOMAIN
from universalassistant.config_entries import ConfigFlowResult
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def _finish_flow(hass: __HAC_KEEP__, flow_id: str) -> ConfigFlowResult:
    """Log in successfully and select the location."""
    with (
        patch("lacrosse_view.LaCrosse.login", return_value=True),
        patch(
            "lacrosse_view.LaCrosse.get_locations",
            return_value=[Location(id="1", name="Test")],
        ),
    ):
        result = await hass.config_entries.flow.async_configure(
            flow_id, {"username": "test-username", "password": "test-password"}
        )
    assert result["step_id"] == "location"

    result = await hass.config_entries.flow.async_configure(flow_id, {"location": "1"})
    await hass.async_block_till_done()
    return result


async def test_form(hass: __HAC_KEEP__, mock_setup_entry: AsyncMock) -> None:
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    with (
        patch(
            "lacrosse_view.LaCrosse.login",
            return_value=True,
        ),
        patch(
            "lacrosse_view.LaCrosse.get_locations",
            return_value=[Location(id="1", name="Test")],
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "location"
    assert result2["errors"] is None

    result3 = await hass.config_entries.flow.async_configure(
        result2["flow_id"],
        {
            "location": "1",
        },
    )
    await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["title"] == "Test"
    assert result3["data"] == {
        "username": "test-username",
        "password": "test-password",
        "id": "1",
        "name": "Test",
    }
    assert result3["result"].unique_id == "1"
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_auth_false(hass: __HAC_KEEP__) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "lacrosse_view.LaCrosse.login",
        return_value=False,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}

    result3 = await _finish_flow(hass, result2["flow_id"])
    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_invalid_auth(hass: __HAC_KEEP__) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch("lacrosse_view.LaCrosse.login", side_effect=LoginError):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}

    result3 = await _finish_flow(hass, result2["flow_id"])
    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_login_first(hass: __HAC_KEEP__) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with (
        patch("lacrosse_view.LaCrosse.login", return_value=True),
        patch("lacrosse_view.LaCrosse.get_locations", side_effect=LoginError),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}

    result3 = await _finish_flow(hass, result2["flow_id"])
    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_no_locations(hass: __HAC_KEEP__) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with (
        patch("lacrosse_view.LaCrosse.login", return_value=True),
        patch(
            "lacrosse_view.LaCrosse.get_locations",
            return_value=None,
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "no_locations"}

    result3 = await _finish_flow(hass, result2["flow_id"])
    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_form_unexpected_error(hass: __HAC_KEEP__) -> None:
    """Test we handle invalid auth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    with patch(
        "universalassistant.components.lacrosse_view.config_flow.validate_input",
        side_effect=Exception,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )

    assert result2["type"] is FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}

    result3 = await _finish_flow(hass, result2["flow_id"])
    assert result3["type"] is FlowResultType.CREATE_ENTRY


async def test_already_configured_device(
    hass: __HAC_KEEP__, mock_setup_entry: AsyncMock
) -> None:
    """Test we handle invalid auth."""
    mock_config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            "username": "test-username",
            "password": "test-password",
            "id": "1",
            "name": "Test",
        },
        unique_id="1",
    )
    mock_config_entry.add_to_hass(hass)

    # Now that we did the config once, let's try to do it again,
    # this should raise the abort for already configured device

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    with (
        patch(
            "lacrosse_view.LaCrosse.login",
            return_value=True,
        ),
        patch(
            "lacrosse_view.LaCrosse.get_locations",
            return_value=[Location(id="1", name="Test")],
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": "test-username",
                "password": "test-password",
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "location"
    assert result2["errors"] is None

    result3 = await hass.config_entries.flow.async_configure(
        result2["flow_id"],
        {
            "location": "1",
        },
    )
    await hass.async_block_till_done()

    assert result3["type"] is FlowResultType.ABORT
    assert result3["reason"] == "already_configured"
    assert len(mock_setup_entry.mock_calls) == 0


async def test_reauth(hass: __HAC_KEEP__) -> None:
    """Test reauthentication."""
    data = {
        "username": "test-username",
        "password": "test-password",
        "id": "1",
        "name": "Test",
    }
    mock_config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=data,
        unique_id="1",
        title="Test",
    )
    mock_config_entry.add_to_hass(hass)

    result = await mock_config_entry.start_reauth_flow(hass)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    new_username = "new-username"
    new_password = "new-password"

    with (
        patch("lacrosse_view.LaCrosse.login", return_value=True),
        patch(
            "lacrosse_view.LaCrosse.get_locations",
            return_value=[Location(id="1", name="Test")],
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                "username": new_username,
                "password": new_password,
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.ABORT
    assert result2["reason"] == "reauth_successful"

    assert len(hass.config_entries.async_entries()) == 1
    assert hass.config_entries.async_entries()[0].data == {
        "username": new_username,
        "password": new_password,
        "id": "1",
        "name": "Test",
    }
