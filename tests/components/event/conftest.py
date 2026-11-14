"""Fixtures for the event entity component tests."""

import logging

import pytest
from pytest_universalassistant.common import MockEntity, MockPlatform, mock_platform

from universalassistant.components.event import DOMAIN, EventEntity
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import TEST_DOMAIN

_LOGGER = logging.getLogger(__name__)


class MockEventEntity(MockEntity, EventEntity):
    """Mock EventEntity class."""

    @property
    def event_types(self) -> list[str]:
        """Return a list of possible events."""
        return self._handle("event_types")


@pytest.fixture
async def mock_event_platform(hass: UniversalAssistant) -> None:
    """Mock the event entity platform."""

    async def async_setup_platform(
        hass: UniversalAssistant,
        config: ConfigType,
        async_add_entities: AddEntitiesCallback,
        discovery_info: DiscoveryInfoType | None = None,
    ) -> None:
        """Set up test event platform."""
        async_add_entities(
            [
                MockEventEntity(
                    name="doorbell",
                    unique_id="unique_doorbell",
                    event_types=["short_press", "long_press"],
                ),
            ]
        )

    mock_platform(
        hass,
        f"{TEST_DOMAIN}.{DOMAIN}",
        MockPlatform(async_setup_platform=async_setup_platform),
    )
