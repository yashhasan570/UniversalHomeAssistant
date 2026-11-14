"""Provide a text platform for MySensors."""

from typing import override

from universalassistant.components.text import TextEntity
from universalassistant.const import Platform
from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers.dispatcher import async_dispatcher_connect
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import setup_mysensors_platform
from .const import MYSENSORS_DISCOVERY, DiscoveryInfo
from .entity import MySensorsChildEntity
from .models import MySensorsConfigEntry


async def async_setup_entry(
    hass: __HAC_KEEP__,
    config_entry: MySensorsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up this platform for a specific ConfigEntry(==Gateway)."""

    @callback
    def async_discover(discovery_info: DiscoveryInfo) -> None:
        """Discover and add a MySensors text entity."""
        setup_mysensors_platform(
            config_entry,
            Platform.TEXT,
            discovery_info,
            MySensorsText,
            async_add_entities,
        )

    config_entry.async_on_unload(
        async_dispatcher_connect(
            hass,
            MYSENSORS_DISCOVERY.format(config_entry.entry_id, Platform.TEXT),
            async_discover,
        ),
    )


class MySensorsText(MySensorsChildEntity, TextEntity):
    """Representation of the value of a MySensors Text child node."""

    _attr_native_max = 25

    @property
    @override
    def native_value(self) -> str | None:
        """Return the value reported by the text."""
        return self._values.get(self.value_type)

    @override
    async def async_set_value(self, value: str) -> None:
        """Change the value."""
        self.gateway.set_child_value(
            self.node_id, self.child_id, self.value_type, value, ack=1
        )
