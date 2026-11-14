"""The tplink_lte integration."""

import probatio

from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv, issue_registry as ir
from universalassistant.helpers.typing import ConfigType

DOMAIN = "tplink_lte"

CONFIG_SCHEMA = probatio.Schema(
    {DOMAIN: cv.match_all},
    extra=probatio.ALLOW_EXTRA,
)


async def async_setup(hass: UniversalAssistant, config: ConfigType) -> bool:
    """Set up TP-Link LTE component."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
        translation_placeholders={
            "ghsa_url": "https://github.com/advisories/GHSA-h95x-26f3-88hr",
        },
    )
    return True
