"""Family Hub camera for Samsung Refrigerators."""

from typing import override

import probatio
from pyfamilyhublocal import FamilyHubCam

from universalassistant.components.camera import (
    PLATFORM_SCHEMA as CAMERA_PLATFORM_SCHEMA,
    Camera,
)
from universalassistant.const import CONF_IP_ADDRESS, CONF_NAME
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.aiohttp_client import async_get_clientsession
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

DEFAULT_NAME = "FamilyHub Camera"

PLATFORM_SCHEMA = CAMERA_PLATFORM_SCHEMA.extend(
    {
        probatio.Required(CONF_IP_ADDRESS): cv.string,
        probatio.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


async def async_setup_platform(
    hass: __HAC_KEEP__,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Family Hub Camera."""

    address = config.get(CONF_IP_ADDRESS)
    name = config.get(CONF_NAME)

    session = async_get_clientsession(hass)
    family_hub_cam = FamilyHubCam(address, hass.loop, session)

    async_add_entities([FamilyHubCamera(name, family_hub_cam)], True)


class FamilyHubCamera(Camera):
    """The representation of a Family Hub camera."""

    def __init__(self, name, family_hub_cam):
        """Initialize camera component."""
        super().__init__()
        self._name = name
        self.family_hub_cam = family_hub_cam

    @override
    async def async_camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return a still image response."""
        return await self.family_hub_cam.async_get_cam_image()

    @property
    @override
    def name(self):
        """Return the name of this camera."""
        return self._name
