"""Test VoIP config flow."""

from unittest.mock import patch

from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components import voip
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_form_user(hass: __HAC_KEEP__) -> None:
    """Test user form config flow."""

    result = await hass.config_entries.flow.async_init(
        voip.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]

    with patch(
        "universalassistant.components.voip.async_setup_entry",
        return_value=None,
    ) as mock_setup_entry:
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {}
    assert len(mock_setup_entry.mock_calls) == 1


async def test_single_instance(
    hass: __HAC_KEEP__, config_entry: config_entries.ConfigEntry
) -> None:
    """Test that only one instance can be created."""
    result = await hass.config_entries.flow.async_init(
        voip.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "single_instance_allowed"


async def test_options_flow(hass: __HAC_KEEP__) -> None:
    """Test config flow options."""
    config_entry = MockConfigEntry(
        domain=voip.DOMAIN,
        data={},
        unique_id="1234",
    )
    config_entry.add_to_hass(hass)

    assert config_entry.options == {}

    result = await hass.config_entries.options.async_init(
        config_entry.entry_id,
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"

    # Default
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert config_entry.options == {"sip_port": 5060}

    # Manual
    result = await hass.config_entries.options.async_init(
        config_entry.entry_id,
    )
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"sip_port": 5061},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert config_entry.options == {"sip_port": 5061}

    # Manual with user
    result = await hass.config_entries.options.async_init(
        config_entry.entry_id,
    )
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"sip_port": 5061, "sip_user": "HA"},
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert config_entry.options == {"sip_port": 5061, "sip_user": "HA"}

    # Manual remove user
    result = await hass.config_entries.options.async_init(
        config_entry.entry_id,
    )

    assert config_entry.options == {"sip_port": 5061, "sip_user": "HA"}

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={"sip_port": 5060, "sip_user": ""},
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert config_entry.options == {"sip_port": 5060}
