"""Define tests for the GDACS config flow."""

from collections.abc import Generator
from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.gdacs.const import DOMAIN
from universalassistant.const import (
    CONF_LATITUDE,
    CONF_LOCATION,
    CONF_LONGITUDE,
    CONF_RADIUS,
)
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

USER_INPUT = {
    CONF_LOCATION: {
        CONF_LATITUDE: -41.2,
        CONF_LONGITUDE: 174.7,
        CONF_RADIUS: 25000,
    }
}


@pytest.fixture(name="gdacs_setup", autouse=True)
def gdacs_setup_fixture() -> Generator[None]:
    """Mock gdacs entry setup."""
    with patch("universalassistant.components.gdacs.async_setup_entry", return_value=None):
        yield


async def test_duplicate_error(
    hass: UniversalAssistant, config_entry: MockConfigEntry
) -> None:
    """Test that errors are shown when duplicates are added."""

    config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=USER_INPUT
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_show_form(hass: UniversalAssistant) -> None:
    """Test that the form is served with no input."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"


async def test_step_user(hass: UniversalAssistant) -> None:
    """Test that the user step works."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=USER_INPUT
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Global Disaster Alert and Coordination System"
    assert result["data"] == {
        CONF_LOCATION: {
            CONF_LATITUDE: -41.2,
            CONF_LONGITUDE: 174.7,
            CONF_RADIUS: 25000,
        }
    }
    assert result["result"].unique_id == "-41.2, 174.7"
