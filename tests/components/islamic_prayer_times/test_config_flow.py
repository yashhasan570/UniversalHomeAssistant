"""Tests for Islamic Prayer Times config flow."""

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.islamic_prayer_times.const import (
    CONF_CALC_METHOD,
    CONF_LAT_ADJ_METHOD,
    CONF_MIDNIGHT_MODE,
    CONF_SCHOOL,
    DOMAIN,
    NAME,
)
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from . import MOCK_CONFIG, MOCK_USER_INPUT

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def test_flow_works(hass: __HAC_KEEP__) -> None:
    """Test user config."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_USER_INPUT
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == NAME
    assert result["result"].unique_id == "12.34-23.45"


async def test_options(hass: __HAC_KEEP__) -> None:
    """Test updating options."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        title="Islamic Prayer Times",
        data=MOCK_CONFIG,
        options={CONF_CALC_METHOD: "isna"},
    )
    entry.add_to_hass(hass)

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            CONF_CALC_METHOD: "makkah",
            CONF_LAT_ADJ_METHOD: "one_seventh",
            CONF_SCHOOL: "hanafi",
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"][CONF_CALC_METHOD] == "makkah"
    assert result["data"][CONF_LAT_ADJ_METHOD] == "one_seventh"
    assert result["data"][CONF_MIDNIGHT_MODE] == "standard"
    assert result["data"][CONF_SCHOOL] == "hanafi"


async def test_integration_already_configured(hass: __HAC_KEEP__) -> None:
    """Test integration is already configured."""
    entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, options={}, unique_id="12.34-23.45"
    )
    entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_USER_INPUT
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
