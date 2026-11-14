"""Switch platform for the embedded component."""

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType


async def async_setup_platform(
    hass: __HAC_KEEP__,
    config: ConfigType,
    async_add_entities_callback: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Find and return test switches."""
