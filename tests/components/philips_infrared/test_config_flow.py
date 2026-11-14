"""Tests for the Philips Infrared config flow."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.infrared import (
    EMITTER_ENTITY_ID as MOCK_INFRARED_EMITTER_ENTITY_ID,
)

from universalassistant.components.philips_infrared.const import (
    CONF_INFRARED_ENTITY_ID,
    DOMAIN,
)
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("mock_infrared_emitter_entity")
@pytest.mark.parametrize(
    ("entity_name", "expected_title"),
    [
        pytest.param(None, "Philips TV via Test IR emitter", id="original_name"),
        pytest.param(
            "Living room IR", "Philips TV via Living room IR", id="custom_name"
        ),
    ],
)
async def test_user_flow_success(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    entity_name: str | None,
    expected_title: str,
) -> None:
    """Test successful config flow, titled after the emitter entity name."""
    entity_registry.async_update_entity(
        MOCK_INFRARED_EMITTER_ENTITY_ID, name=entity_name
    )

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_INFRARED_ENTITY_ID: MOCK_INFRARED_EMITTER_ENTITY_ID},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == expected_title
    assert result["data"] == {CONF_INFRARED_ENTITY_ID: MOCK_INFRARED_EMITTER_ENTITY_ID}
    assert result["result"].unique_id is None


@pytest.mark.usefixtures("mock_infrared_emitter_entity")
async def test_user_flow_already_configured(
    hass: __HAC_KEEP__, mock_config_entry: MockConfigEntry
) -> None:
    """Test flow aborts when the emitter is already used by another entry."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_INFRARED_ENTITY_ID: MOCK_INFRARED_EMITTER_ENTITY_ID},
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


@pytest.mark.usefixtures("init_infrared")
async def test_user_flow_no_emitters(hass: __HAC_KEEP__) -> None:
    """Test flow aborts when no infrared emitters exist."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_infrared_emitters"
