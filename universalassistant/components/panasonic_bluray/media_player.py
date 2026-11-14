"""Support for Panasonic Blu-ray players."""

from datetime import timedelta
from typing import override

from panacotta import PanasonicBD
import probatio

from universalassistant.components.media_player import (
    PLATFORM_SCHEMA as MEDIA_PLAYER_PLATFORM_SCHEMA,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
)
from universalassistant.const import CONF_HOST, CONF_NAME
from universalassistant.core import UniversalAssistant
from universalassistant.helpers import config_validation as cv
from universalassistant.helpers.entity_platform import AddEntitiesCallback
from universalassistant.helpers.typing import ConfigType, DiscoveryInfoType
from universalassistant.util.dt import utcnow

DEFAULT_NAME = "Panasonic Blu-Ray"

SCAN_INTERVAL = timedelta(seconds=30)


PLATFORM_SCHEMA = MEDIA_PLAYER_PLATFORM_SCHEMA.extend(
    {
        probatio.Required(CONF_HOST): cv.string,
        probatio.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


def setup_platform(
    hass: UniversalAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Panasonic Blu-ray media player platform."""
    conf = discovery_info or config

    # Register configured device with Universal Universal Home Assistant.
    add_entities([PanasonicBluRay(conf[CONF_HOST], conf[CONF_NAME])])


class PanasonicBluRay(MediaPlayerEntity):
    """Representation of a Panasonic Blu-ray device."""

    _attr_icon = "mdi:disc-player"
    _attr_supported_features = (
        MediaPlayerEntityFeature.TURN_ON
        | MediaPlayerEntityFeature.TURN_OFF
        | MediaPlayerEntityFeature.PLAY
        | MediaPlayerEntityFeature.STOP
        | MediaPlayerEntityFeature.PAUSE
    )

    def __init__(self, ip, name):
        """Initialize the Panasonic Blu-ray device."""
        self._device = PanasonicBD(ip)
        self._attr_name = name
        self._attr_state = MediaPlayerState.OFF
        self._attr_media_position = 0
        self._attr_media_duration = 0

    def update(self) -> None:
        """Update the internal state by querying the device."""
        # This can take 5+ seconds to complete
        state = self._device.get_play_status()

        if state[0] == "error":
            self._attr_state = None
        elif state[0] in ["off", "standby"]:
            # We map both of these to off. If it's really off we can't
            # turn it on, but from standby we can go to idle by pressing
            # POWER.
            self._attr_state = MediaPlayerState.OFF
        elif state[0] in ["paused", "stopped"]:
            self._attr_state = MediaPlayerState.IDLE
        elif state[0] == "playing":
            self._attr_state = MediaPlayerState.PLAYING

        # Update our current media position + length
        if state[1] >= 0:
            self._attr_media_position = state[1]
        else:
            self._attr_media_position = 0
        self._attr_media_position_updated_at = utcnow()
        self._attr_media_duration = state[2]

    @override
    def turn_off(self) -> None:
        """Instruct the device to turn standby.

        Sending the "POWER" button will turn the device to standby - there
        is no way to turn it completely off remotely. However this works in
        our favour as it means the device is still accepting commands and we
        can thus turn it back on when desired.
        """
        if self.state != MediaPlayerState.OFF:
            self._device.send_key("POWER")

        self._attr_state = MediaPlayerState.OFF

    @override
    def turn_on(self) -> None:
        """Wake the device back up from standby."""
        if self.state == MediaPlayerState.OFF:
            self._device.send_key("POWER")

        self._attr_state = MediaPlayerState.IDLE

    @override
    def media_play(self) -> None:
        """Send play command."""
        self._device.send_key("PLAYBACK")

    @override
    def media_pause(self) -> None:
        """Send pause command."""
        self._device.send_key("PAUSE")

    @override
    def media_stop(self) -> None:
        """Send stop command."""
        self._device.send_key("STOP")
