"""Coordinator for the Tile BLE integration."""

import logging
from typing import TYPE_CHECKING

from universalassistant.components.bluetooth import BluetoothScanningMode
from universalassistant.components.bluetooth.passive_update_coordinator import (
    PassiveBluetoothDataUpdateCoordinator,
)
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import UniversalAssistant

_LOGGER = logging.getLogger(__name__)

type TileBleConfigEntry = ConfigEntry[TileBleCoordinator]


class TileBleCoordinator(PassiveBluetoothDataUpdateCoordinator):
    """Track the advertisements of a Tile."""

    def __init__(self, hass: UniversalAssistant, config_entry: TileBleConfigEntry) -> None:
        """Initialize the coordinator."""
        if TYPE_CHECKING:
            assert config_entry.unique_id is not None
        super().__init__(
            hass,
            _LOGGER,
            config_entry.unique_id,
            BluetoothScanningMode.PASSIVE,
            connectable=False,
        )
        self.config_entry = config_entry
