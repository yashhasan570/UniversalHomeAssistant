"""Fixtures for Climate platform tests."""

from collections.abc import Generator

import pytest
from pytest_universalassistant.common import (
    MockConfigEntry,
    MockModule,
    mock_config_flow,
    mock_integration,
    mock_platform,
)

from universalassistant.config_entries import ConfigEntry, ConfigFlow
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__


class MockFlow(ConfigFlow):
    """Test flow."""


@pytest.fixture
def config_flow_fixture(hass: __HAC_KEEP__) -> Generator[None]:
    """Mock config flow."""
    mock_platform(hass, "test.config_flow")

    with mock_config_flow("test", MockFlow):
        yield


@pytest.fixture
def register_test_integration(
    hass: __HAC_KEEP__, config_flow_fixture: None
) -> Generator:
    """Provide a mocked integration for tests."""

    config_entry = MockConfigEntry(domain="test")
    config_entry.add_to_hass(hass)

    async def help_async_setup_entry_init(
        hass: __HAC_KEEP__, config_entry: ConfigEntry
    ) -> None:
        """Set up test config entry."""
        await hass.config_entries.async_forward_entry_setups(
            config_entry, [Platform.CLIMATE]
        )

    async def help_async_unload_entry(
        hass: __HAC_KEEP__, config_entry: ConfigEntry
    ) -> None:
        """Unload test config emntry."""
        await hass.config_entries.async_unload_platforms_or_raise(
            config_entry, [Platform.CLIMATE]
        )

    mock_integration(
        hass,
        MockModule(
            "test",
            async_setup_entry=help_async_setup_entry_init,
            async_unload_entry=help_async_unload_entry,
        ),
    )

    return config_entry
