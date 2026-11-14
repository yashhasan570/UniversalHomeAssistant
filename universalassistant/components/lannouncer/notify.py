"""Lannouncer platform for notify component."""

import probatio

from universalassistant.components.notify import PLATFORM_SCHEMA as NOTIFY_PLATFORM_SCHEMA
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import issue_registry as ir
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

DOMAIN = "lannouncer"

PLATFORM_SCHEMA = NOTIFY_PLATFORM_SCHEMA.extend({}, extra=probatio.ALLOW_EXTRA)


async def async_get_service(
    hass: __HAC_KEEP__,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Get the Lannouncer notification service."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
    )
