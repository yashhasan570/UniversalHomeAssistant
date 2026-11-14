"""Test the Pico TTS config flow."""

from unittest.mock import AsyncMock

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant import config_entries
from universalassistant.components.picotts.const import DOMAIN
from universalassistant.components.tts import CONF_LANG
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


async def test_user_step(hass: __HAC_KEEP__, mock_setup_entry: AsyncMock) -> None:
    """Test user step create entry result."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_LANG: "es-ES",
        },
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Pico TTS es-ES"
    assert result["data"] == {
        CONF_LANG: "es-ES",
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_already_configured(
    hass: __HAC_KEEP__, mock_setup_entry: AsyncMock
) -> None:
    """Test user step already configured entry."""
    config_entry = MockConfigEntry(domain=DOMAIN, data={CONF_LANG: "es-ES"})
    config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_LANG: "es-ES",
        },
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
    assert len(mock_setup_entry.mock_calls) == 0
