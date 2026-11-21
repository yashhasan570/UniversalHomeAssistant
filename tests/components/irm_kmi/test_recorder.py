"""Tests for the IRM KMI recorder exclusions."""

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.components.recorder.common import async_wait_recording_done

from universalassistant.components.recorder.history import get_significant_states
from universalassistant.core import UniversalAssistant
from universalassistant.util import dt as dt_util

from . import setup_integration
from .const import WARNING_ENTITY_ID


@pytest.mark.usefixtures("recorder_mock", "mock_irm_kmi_api")
async def test_exclude_attributes(
    hass: UniversalAssistant, mock_config_entry: MockConfigEntry
) -> None:
    """Test the warnings are not recorded."""
    now = dt_util.utcnow()
    await setup_integration(hass, mock_config_entry)
    assert "warnings" in hass.states.get(WARNING_ENTITY_ID).attributes
    await async_wait_recording_done(hass)

    states = await hass.async_add_executor_job(
        get_significant_states, hass, now, None, [WARNING_ENTITY_ID]
    )
    assert len(states[WARNING_ENTITY_ID]) == 1
    assert "warnings" not in states[WARNING_ENTITY_ID][0].attributes
