"""The OpenThread Border Router integration types."""

from universalassistant.config_entries import ConfigEntry

from .util import OTBRData

type OTBRConfigEntry = ConfigEntry[OTBRData]
