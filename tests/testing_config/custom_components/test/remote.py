"""Provide a mock remote platform.

Call init before using it in your tests to ensure clean test data.
"""

from pytest_universalassistant.common import MockToggleEntity

from universalassistant.components.remote import RemoteEntity
from universalassistant.const import STATE_OFF, STATE_ON
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

ENTITIES = []


def init(empty=False):
    """Initialize the platform with entities."""
    # pylint: disable-next=global-statement
    global ENTITIES  # noqa: PLW0603

    ENTITIES = (
        []
        if empty
        else [
            MockRemote("TV", STATE_ON),
            MockRemote("DVD", STATE_OFF),
            MockRemote(None, STATE_OFF),
        ]
    )


async def async_setup_platform(
    hass: __HAC_KEEP__,
    config: ConfigType,
    async_add_entities_callback: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Return mock entities."""
    async_add_entities_callback(ENTITIES)


class MockRemote(MockToggleEntity, RemoteEntity):
    """Mock remote class."""

    supported_features = 0
