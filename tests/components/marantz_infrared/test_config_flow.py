"""Tests for the Marantz Infrared config flow."""

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.marantz_infrared.const import (
    CONF_INFRARED_EMITTER_ENTITY_ID,
    DOMAIN,
)
from universalassistant.config_entries import SOURCE_USER
from universalassistant.const import CONF_MODEL
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

from .conftest import MOCK_INFRARED_EMITTER_ENTITY_ID


@pytest.mark.usefixtures("mock_infrared_emitter_entity")
async def test_user_flow_success(
    hass: __HAC_KEEP__,
) -> None:
    """Test successful user config flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MODEL: "pm6006_integrated_amplifier",
            CONF_INFRARED_EMITTER_ENTITY_ID: MOCK_INFRARED_EMITTER_ENTITY_ID,
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "PM6006 Integrated Amplifier"
    assert result["data"] == {
        CONF_MODEL: "pm6006_integrated_amplifier",
        CONF_INFRARED_EMITTER_ENTITY_ID: MOCK_INFRARED_EMITTER_ENTITY_ID,
    }
    assert (
        result["result"].unique_id
        == f"pm6006_integrated_amplifier_{MOCK_INFRARED_EMITTER_ENTITY_ID}"
    )


@pytest.mark.usefixtures("mock_infrared_emitter_entity")
async def test_user_flow_already_configured(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test user flow aborts when entry is already configured."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MODEL: "pm6006_integrated_amplifier",
            CONF_INFRARED_EMITTER_ENTITY_ID: MOCK_INFRARED_EMITTER_ENTITY_ID,
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


@pytest.mark.usefixtures("init_infrared")
async def test_user_flow_no_emitters(hass: __HAC_KEEP__) -> None:
    """Test user flow aborts when no infrared emitters exist."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_emitters"


@pytest.mark.usefixtures("mock_infrared_emitter_entity")
@pytest.mark.parametrize(
    ("model", "expected_title"),
    [
        ("generic_amplifier", "Generic Amplifier"),
        ("pm6006_integrated_amplifier", "PM6006 Integrated Amplifier"),
    ],
)
async def test_user_flow_title_from_model(
    hass: __HAC_KEEP__, model: str, expected_title: str
) -> None:
    """Test config entry title is the model name."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={
            CONF_MODEL: model,
            CONF_INFRARED_EMITTER_ENTITY_ID: MOCK_INFRARED_EMITTER_ENTITY_ID,
        },
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == expected_title
    assert result["result"].unique_id == f"{model}_{MOCK_INFRARED_EMITTER_ENTITY_ID}"
