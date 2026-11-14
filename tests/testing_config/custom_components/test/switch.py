"""Stub switch platform for translation tests."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: __HAC_KEEP__,
    config: ConfigType,
    async_add_entities_callback: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Stub setup for translation tests."""
    async_add_entities_callback([])
