"""Fixtures for the Timer list component tests."""

from collections.abc import Generator

import pytest
from pytest_universalassistant.common import (
    MockModule,
    mock_config_flow,
    mock_integration,
    mock_platform,
)

from universalassistant.components.timer_list import TimerListEntity
from universalassistant.config_entries import ConfigEntry
from universalassistant.const import Platform
from universalassistant.core import UniversalAssistant

from . import TEST_DOMAIN, MockFlow, MockTimerListEntity, create_mock_platform


@pytest.fixture(autouse=True)
def config_flow_fixture(hass: UniversalAssistant) -> Generator[None]:
    """Mock config flow."""
    mock_platform(hass, f"{TEST_DOMAIN}.config_flow")

    with mock_config_flow(TEST_DOMAIN, MockFlow):
        yield


@pytest.fixture(autouse=True)
def mock_setup_integration(hass: UniversalAssistant) -> None:
    """Fixture to set up a mock integration."""

    async def async_setup_entry_init(
        hass: UniversalAssistant, config_entry: ConfigEntry
    ) -> None:
        """Set up test config entry."""
        await hass.config_entries.async_forward_entry_setups(
            config_entry, [Platform.TIMER_LIST]
        )

    async def async_unload_entry_init(
        hass: UniversalAssistant, config_entry: ConfigEntry
    ) -> None:
        await hass.config_entries.async_unload_platforms(
            config_entry, [Platform.TIMER_LIST]
        )

    mock_integration(
        hass,
        MockModule(
            TEST_DOMAIN,
            async_setup_entry=async_setup_entry_init,
            async_unload_entry=async_unload_entry_init,
        ),
    )


@pytest.fixture(name="test_entity")
async def mock_test_entity(hass: UniversalAssistant) -> TimerListEntity:
    """Fixture that creates a test timer list entity."""
    entity = MockTimerListEntity()
    entity.entity_id = "timer_list.timers"
    await create_mock_platform(hass, [entity])
    return entity
