"""Microsoft Teams platform for notify component."""

import probatio

from universalassistant.components.notify import PLATFORM_SCHEMA as NOTIFY_PLATFORM_SCHEMA
from universalassistant.const import CONF_URL
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv, issue_registry as ir
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

DOMAIN = "msteams"

PLATFORM_SCHEMA = NOTIFY_PLATFORM_SCHEMA.extend({probatio.Required(CONF_URL): cv.url})


async def async_get_service(
    hass: UniversalAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Get the Microsoft Teams notification service."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
        translation_placeholders={
            "url": "https://devblogs.microsoft.com/microsoft365dev/retirement-of-office-365-connectors-within-microsoft-teams/"
        },
    )
