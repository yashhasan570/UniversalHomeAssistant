"""Constants for the Backup integration."""

from logging import getLogger
from typing import TYPE_CHECKING

from universalassistant.util.hass_dict import HassKey

if TYPE_CHECKING:
    from .manager import BackupManager

BUF_SIZE = 2**20 * 4  # 4MB
DOMAIN = "backup"
DATA_MANAGER: HassKey[BackupManager] = HassKey(DOMAIN)
LOGGER = getLogger(__package__)

EXCLUDE_FROM_BACKUP = [
    "**/__pycache__/*",
    "**/.DS_Store",
    ".HA_RESTORE",
    "*.db-shm",
    "*.log.*",
    "*.log",
    "backups/*.tar",
    "tmp_backups/*.tar",
    "OZW_Log.txt",
    "tts/*",
    ".cache/*",
]

EXCLUDE_DATABASE_FROM_BACKUP = [
    "universal-assistant_v2.db",
    "universal-assistant_v2.db-wal",
]

SECURETAR_CREATE_VERSION = 3
