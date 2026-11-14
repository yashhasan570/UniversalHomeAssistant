"""Support for Zengge lights."""

import probatio

from universalassistant.components.light import PLATFORM_SCHEMA as LIGHT_PLATFORM_SCHEMA
from universalassistant.const import CONF_DEVICES, CONF_NAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv, issue_registry as ir
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

DEVICE_SCHEMA = probatio.Schema({probatio.Optional(CONF_NAME): cv.string})
DOMAIN = "zengge"

PLATFORM_SCHEMA = LIGHT_PLATFORM_SCHEMA.extend(
    {probatio.Optional(CONF_DEVICES, default={}): {cv.string: DEVICE_SCHEMA}}
)


async def async_setup_platform(
    hass: __HAC_KEEP__,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Zengge platform."""
    ir.async_create_issue(
        hass,
        DOMAIN,
        DOMAIN,
        is_fixable=False,
        severity=ir.IssueSeverity.ERROR,
        translation_key="integration_removed",
        translation_placeholders={
            "led_ble_url": "https://www.universalassistant.io/integrations/led_ble/",
        },
    )
