"""Generate the device_classes.json file."""

import json

from hassfest.model import Config, Integration

from universalassistant.components.binary_sensor import BinarySensorDeviceClass
from universalassistant.components.button import ButtonDeviceClass
from universalassistant.components.cover import CoverDeviceClass
from universalassistant.components.event import EventDeviceClass
from universalassistant.components.humidifier import HumidifierDeviceClass
from universalassistant.components.infrared import InfraredDeviceClass
from universalassistant.components.media_player import MediaPlayerDeviceClass
from universalassistant.components.number import NumberDeviceClass
from universalassistant.components.radio_frequency import RadioFrequencyDeviceClass
from universalassistant.components.sensor import SensorDeviceClass
from universalassistant.components.switch import SwitchDeviceClass
from universalassistant.components.update import UpdateDeviceClass
from universalassistant.components.valve import ValveDeviceClass
from universalassistant.const import Platform

PATH = "universalassistant/generated/device_classes.json"


def _generate() -> str:
    """Generate the device classes data."""
    return json.dumps(
        {
            domain.value: sorted(device_class.value for device_class in device_classes)
            for domain, device_classes in {
                Platform.BINARY_SENSOR: BinarySensorDeviceClass,
                Platform.BUTTON: ButtonDeviceClass,
                Platform.COVER: CoverDeviceClass,
                Platform.EVENT: EventDeviceClass,
                Platform.HUMIDIFIER: HumidifierDeviceClass,
                Platform.INFRARED: InfraredDeviceClass,
                Platform.MEDIA_PLAYER: MediaPlayerDeviceClass,
                Platform.NUMBER: NumberDeviceClass,
                Platform.RADIO_FREQUENCY: RadioFrequencyDeviceClass,
                Platform.SENSOR: SensorDeviceClass,
                Platform.SWITCH: SwitchDeviceClass,
                Platform.UPDATE: UpdateDeviceClass,
                Platform.VALVE: ValveDeviceClass,
            }.items()
        },
        indent=2,
    )


def validate(integrations: dict[str, Integration], config: Config) -> None:
    """Validate device_classes.json."""
    path = config.root / PATH
    config.cache["device_classes"] = content = _generate()

    if path.read_text() != content + "\n":
        config.add_error(
            "device_classes",
            "File device_classes.json is not up to date. Run python3 -m script.hassfest",
            fixable=True,
        )


def generate(integrations: dict[str, Integration], config: Config) -> None:
    """Generate device_classes.json."""
    path = config.root / PATH
    path.write_text(f"{config.cache['device_classes']}\n")
