"""Support for Tellstick covers using Tellstick Net."""

from typing import Any, override

from universalassistant.components import cover
from universalassistant.components.cover import CoverEntity
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.dispatcher import async_dispatcher_connect
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import TelldusLiveConfigEntry
from .const import DOMAIN, TELLDUS_DISCOVERY_NEW
from .entity import TelldusLiveEntity


async def async_setup_entry(
    hass: UniversalAssistant,
    config_entry: TelldusLiveConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up tellduslive sensors dynamically."""

    async def async_discover_cover(device_id):
        """Discover and add a discovered sensor."""
        client = config_entry.runtime_data.client
        async_add_entities([TelldusLiveCover(client, device_id)])

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            TELLDUS_DISCOVERY_NEW.format(cover.DOMAIN, DOMAIN),
            async_discover_cover,
        )
    )


class TelldusLiveCover(TelldusLiveEntity, CoverEntity):
    """Representation of a cover."""

    _attr_name = None

    @property
    @override
    def is_closed(self) -> bool:
        """Return the current position of the cover."""
        return self.device.is_down

    @override
    def close_cover(self, **kwargs: Any) -> None:
        """Close the cover."""
        self.device.down()
        self.schedule_update_ha_state()

    @override
    def open_cover(self, **kwargs: Any) -> None:
        """Open the cover."""
        self.device.up()
        self.schedule_update_ha_state()

    @override
    def stop_cover(self, **kwargs: Any) -> None:
        """Stop the cover."""
        self.device.stop()
        self.schedule_update_ha_state()
