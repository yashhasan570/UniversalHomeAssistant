"""Support for esphome domain data."""

from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cache

from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.json import JSONEncoder

from .const import ESPHOME_DATA
from .entry_data import ESPHomeConfigEntry, ESPHomeStorage, RuntimeEntryData

STORAGE_VERSION = 1


@dataclass(slots=True)
class DomainData:
    """Define a class that stores global esphome data."""

    _stores: dict[str, ESPHomeStorage] = field(default_factory=dict)
    sendspin_client_ids: dict[str, str] = field(default_factory=dict)
    sendspin_subscribers: set[Callable[[list[str]], None]] = field(default_factory=set)

    def get_entry_data(self, entry: ESPHomeConfigEntry) -> RuntimeEntryData:
        """Return the runtime entry data associated with this config entry."""
        return entry.runtime_data

    def get_or_create_store(
        self, hass: __HAC_KEEP__, entry: ESPHomeConfigEntry
    ) -> ESPHomeStorage:
        """Get or create a Store instance for the given config entry."""
        return self._stores.setdefault(
            entry.entry_id,
            ESPHomeStorage(
                hass, STORAGE_VERSION, f"esphome.{entry.entry_id}", encoder=JSONEncoder
            ),
        )

    @staticmethod
    @cache
    def get(hass: __HAC_KEEP__) -> DomainData:
        """Get the global DomainData instance stored in hass.data."""
        ret = hass.data[ESPHOME_DATA] = DomainData()
        return ret
