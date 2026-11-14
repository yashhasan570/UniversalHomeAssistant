"""Tests for IPMA config flow."""

from collections.abc import Generator
from unittest.mock import patch

from pyipma import IPMAException
import pytest

from universalassistant.components.ipma.const import DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_LATITUDE, CONF_LOCATION, CONF_LONGITUDE
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

from . import MockLocation

USER_INPUT = {
    CONF_LOCATION: {
        CONF_LONGITUDE: 0,
        CONF_LATITUDE: 0,
    }
}


@pytest.fixture(name="ipma_setup", autouse=True)
def ipma_setup_fixture() -> Generator[None]:
    """Patch ipma setup entry."""
    with patch("universalassistant.components.ipma.async_setup_entry", return_value=None):
        yield


async def test_config_flow(hass: UniversalAssistant) -> None:
    """Test configuration form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "pyipma.location.Location.get",
        return_value=MockLocation(),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=USER_INPUT,
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "HomeTown"
    assert result["data"] == {
        CONF_LONGITUDE: 0,
        CONF_LATITUDE: 0,
    }


async def test_config_flow_failures(hass: UniversalAssistant) -> None:
    """Test config flow with failures."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    with patch(
        "pyipma.location.Location.get",
        side_effect=IPMAException(),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=USER_INPUT,
        )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "unknown"}
    with patch(
        "pyipma.location.Location.get",
        return_value=MockLocation(),
    ):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=USER_INPUT,
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "HomeTown"
    assert result["data"] == {
        CONF_LONGITUDE: 0,
        CONF_LATITUDE: 0,
    }


@pytest.mark.usefixtures("init_integration")
async def test_flow_entry_already_exists(hass: UniversalAssistant) -> None:
    """Test user input for config_entry that already exists.

    Test when the form should show when user puts existing location
    in the config gui. Then the form should show with error.
    """
    result = await hass.config_entries.flow.async_init(
        DOMAIN,
        context={"source": SOURCE_USER},
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=USER_INPUT
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
