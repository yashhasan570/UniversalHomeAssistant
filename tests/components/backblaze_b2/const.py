"""Consts for Backblaze B2 tests."""

from universalassistant.components.backblaze_b2.const import CONF_BUCKET
from universalassistant.components.backup import AgentBackup
from universalassistant.const import CONF_PREFIX

USER_INPUT = {
    CONF_BUCKET: "testBucket",
    CONF_PREFIX: "testprefix/",
}


TEST_BACKUP = AgentBackup(
    addons=[],
    backup_id="23e64aec",
    date="2024-11-22T11:48:48.727189+01:00",
    database_included=True,
    extra_metadata={},
    folders=[],
    universalassistant_included=True,
    universalassistant_version="2024.12.0.dev0",
    name="Core 2024.12.0.dev0",
    protected=False,
    size=48,
)

BACKUP_METADATA = {
    "metadata_version": "1",
    "backup_id": "23e64aec",
    "backup_metadata": TEST_BACKUP.as_dict(),
}

METADATA_FILE_SUFFIX = ".metadata.json"
