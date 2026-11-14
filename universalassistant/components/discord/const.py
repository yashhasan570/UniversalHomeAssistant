"""Constants for the Discord integration."""

from typing import Final

from universalassistant.const import CONF_URL

DEFAULT_NAME = "Discord"
DOMAIN: Final = "discord"

CONF_ENTRY: Final = "entry"
CONF_TARGET_ID: Final = "target_id"
SUBENTRY_TYPE_TARGET: Final = "target"

URL_PLACEHOLDER = {CONF_URL: "https://www.universalassistant.io/integrations/discord"}

DATA_HASS_CONFIG = "discord_hass_config"
