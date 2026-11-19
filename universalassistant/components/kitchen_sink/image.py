"""Demo image platform."""

from dataclasses import dataclass
from pathlib import Path
from typing import override

from universalassistant.components.image import ImageEntity, ImageEntityDescription
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import (
    AddConfigEntryEntitiesCallback,
    AddEntitiesCallback,
)
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType
from universalassistant.util import dt as dt_util


@dataclass(frozen=True, kw_only=True)
class DemoImageEntityDescription(ImageEntityDescription):
    """Describes a demo image."""

    content_type: str
    image: str


IMAGES = (
    DemoImageEntityDescription(
        key="kitchen_sink_image_001",
        name="QR Code",
        content_type="image/png",
        image="qr_code.png",
    ),
)


async def async_setup_platform(
    hass: UniversalAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up image entities."""
    async_add_entities(DemoImage(hass, description) for description in IMAGES)


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the Everything but the Kitchen Sink config entry."""
    await async_setup_platform(hass, {}, async_add_entities)


class DemoImage(ImageEntity):
    """Representation of an image entity."""

    entity_description: DemoImageEntityDescription

    def __init__(
        self, hass: UniversalAssistant, description: DemoImageEntityDescription
    ) -> None:
        """Initialize the image entity."""
        super().__init__(hass)
        self.entity_description = description
        self._attr_content_type = description.content_type
        self._attr_unique_id = description.key

    @override
    async def async_added_to_hass(self) -> None:
        """Set the update time."""
        self._attr_image_last_updated = dt_util.utcnow()

    @override
    async def async_image(self) -> bytes | None:
        """Return bytes of image."""
        image_path = Path(__file__).parent / self.entity_description.image
        return await self.hass.async_add_executor_job(image_path.read_bytes)
