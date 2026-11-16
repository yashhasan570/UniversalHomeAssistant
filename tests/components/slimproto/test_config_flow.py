"""Test the SlimProto Player config flow."""

from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.slimproto.const import DEFAULT_NAME, DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType


async def test_full_user_flow(hass: UniversalAssistant, mock_setup_entry: AsyncMock) -> None:
    """Test the full user configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result.get("type") is FlowResultType.CREATE_ENTRY
    assert result.get("title") == DEFAULT_NAME
    assert result.get("data") == {}

    assert len(mock_setup_entry.mock_calls) == 1


@pytest.mark.usefixtures("mock_setup_entry")
async def test_already_configured(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test abort if SlimProto Player is already configured."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    assert result.get("type") is FlowResultType.ABORT
    assert result.get("reason") == "single_instance_allowed"
