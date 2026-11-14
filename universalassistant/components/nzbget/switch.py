"""Support for NZBGet switches."""

from typing import Any, override

from universalassistant.components.switch import SwitchEntity
from universalassistant.const import CONF_NAME
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import NZBGetConfigEntry, NZBGetDataUpdateCoordinator
from .entity import NZBGetEntity


async def async_setup_entry(
    hass: UniversalAssistant,
    entry: NZBGetConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up NZBGet switch based on a config entry."""
    coordinator = entry.runtime_data

    switches = [
        NZBGetDownloadSwitch(
            coordinator,
            entry.entry_id,
            entry.data.get(CONF_NAME, entry.title),
        ),
    ]

    async_add_entities(switches)


class NZBGetDownloadSwitch(NZBGetEntity, SwitchEntity):
    """Representation of a NZBGet download switch."""

    _attr_translation_key = "download"

    def __init__(
        self,
        coordinator: NZBGetDataUpdateCoordinator,
        entry_id: str,
        entry_name: str,
    ) -> None:
        """Initialize a new NZBGet switch."""
        self._attr_unique_id = f"{entry_id}_download"

        super().__init__(
            coordinator=coordinator,
            entry_id=entry_id,
            entry_name=entry_name,
        )

    @property
    @override
    def is_on(self) -> bool:
        """Return the state of the switch."""
        return not self.coordinator.data["status"].get("DownloadPaused", False)

    @override
    async def async_turn_on(self, **kwargs: Any) -> None:
        """Set downloads to enabled."""
        await self.hass.async_add_executor_job(self.coordinator.nzbget.resumedownload)
        await self.coordinator.async_request_refresh()

    @override
    async def async_turn_off(self, **kwargs: Any) -> None:
        """Set downloads to paused."""
        await self.hass.async_add_executor_job(self.coordinator.nzbget.pausedownload)
        await self.coordinator.async_request_refresh()
