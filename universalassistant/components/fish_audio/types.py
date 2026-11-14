"""Type definitions for the Fish Audio integration."""

from fishaudio import AsyncFishAudio

from universalassistant.config_entries import ConfigEntry

type FishAudioConfigEntry = ConfigEntry[AsyncFishAudio]
