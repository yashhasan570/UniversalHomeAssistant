"""Fixtures for history tests."""

import pytest
from pytest_universalassistant.typing import RecorderInstanceContextManager

from universalassistant.components import history
from universalassistant.components.recorder import Recorder
from universalassistant.const import CONF_DOMAINS, CONF_ENTITIES, CONF_EXCLUDE, CONF_INCLUDE
from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component


@pytest.fixture
async def mock_recorder_before_hass(
    async_test_recorder: RecorderInstanceContextManager,
) -> None:
    """Set up recorder."""


@pytest.fixture
async def hass_history(hass: UniversalAssistant, recorder_mock: Recorder) -> None:
    """Universal Home Assistant fixture with history."""
    config = history.CONFIG_SCHEMA(
        {
            history.DOMAIN: {
                CONF_INCLUDE: {
                    CONF_DOMAINS: ["media_player"],
                    CONF_ENTITIES: ["thermostat.test"],
                },
                CONF_EXCLUDE: {
                    CONF_DOMAINS: ["thermostat"],
                    CONF_ENTITIES: ["media_player.test"],
                },
            }
        }
    )
    assert await async_setup_component(hass, history.DOMAIN, config)
