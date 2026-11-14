"""Constants for Bravia TV integration."""

from enum import StrEnum
from typing import Final

ATTR_CID: Final = "cid"
ATTR_MAC: Final = "macAddr"
ATTR_MANUFACTURER: Final = "Sony"

CONF_NICKNAME: Final = "nickname"
CONF_USE_PSK: Final = "use_psk"
CONF_USE_SSL: Final = "use_ssl"

DOMAIN: Final = "braviatv"
LEGACY_CLIENT_ID: Final = "__HAC_KEEP__"
NICKNAME_PREFIX: Final = "__HA_KEEP__"


class SourceType(StrEnum):
    """Source type for Sony TV Integration."""

    APP = "app"
    CHANNEL = "channel"
    INPUT = "input"
