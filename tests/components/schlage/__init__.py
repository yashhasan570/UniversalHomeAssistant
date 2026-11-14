"""Tests for the Schlage integration."""

from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.schlage.coordinator import SchlageDataUpdateCoordinator

type MockSchlageConfigEntry = MockConfigEntry[SchlageDataUpdateCoordinator]
