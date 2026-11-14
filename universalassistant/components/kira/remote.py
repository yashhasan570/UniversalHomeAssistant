"""Support for Keene Electronics IR-IP devices."""

from collections.abc import Iterable
import logging
from typing import Any, override

from universalassistant.components import remote
from universalassistant.const import CONF_DEVICE, CONF_NAME
from universalassistant.core import UniversalAssistant
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import CONF_REMOTE, DOMAIN

_LOGGER = logging.getLogger(__name__)


def setup_platform(
    hass: UniversalAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Kira platform."""
    if discovery_info:
        name = discovery_info.get(CONF_NAME)
        device = discovery_info.get(CONF_DEVICE)

        kira = hass.data[DOMAIN][CONF_REMOTE][name]
        add_entities([KiraRemote(device, kira)])


class KiraRemote(remote.RemoteEntity):
    """Remote representation used to send commands to a Kira device."""

    def __init__(self, name, kira):
        """Initialize KiraRemote class."""
        _LOGGER.debug("KiraRemote device init started for: %s", name)
        self._attr_name = name
        self._kira = kira

    @override
    def send_command(self, command: Iterable[str], **kwargs: Any) -> None:
        """Send a command to one device."""
        for single_command in command:
            code_tuple = (single_command, kwargs.get(remote.ATTR_DEVICE))
            _LOGGER.debug("Sending Command: %s to %s", *code_tuple)
            self._kira.sendCode(code_tuple)
