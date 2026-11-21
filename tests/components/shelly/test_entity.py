"""Tests for Shelly entity helpers."""

import pytest

from universalassistant.components.shelly.binary_sensor import (
    RPC_SENSORS as RPC_BINARY_SENSORS,
)
from universalassistant.components.shelly.button import RPC_BUTTONS
from universalassistant.components.shelly.camera import RPC_CAMERA_ENTITIES
from universalassistant.components.shelly.climate import RPC_LINKEDGO_THERMOSTAT
from universalassistant.components.shelly.cover import RPC_COVERS
from universalassistant.components.shelly.entity import (
    RpcEntityDescription,
    get_rpc_descriptions_by_attribute,
)
from universalassistant.components.shelly.fan import RPC_FANS
from universalassistant.components.shelly.infrared import RPC_INFRARED_ENTITIES
from universalassistant.components.shelly.light import LIGHTS
from universalassistant.components.shelly.media_player import RPC_MEDIA_PLAYER_ENTITIES
from universalassistant.components.shelly.number import RPC_NUMBERS
from universalassistant.components.shelly.select import RPC_SELECT_ENTITIES
from universalassistant.components.shelly.sensor import RPC_SENSORS
from universalassistant.components.shelly.switch import RPC_SWITCHES
from universalassistant.components.shelly.text import RPC_TEXT_ENTITIES
from universalassistant.components.shelly.update import RPC_UPDATES
from universalassistant.components.shelly.valve import RPC_VALVES


@pytest.mark.parametrize(
    "descriptions",
    [
        pytest.param(RPC_BINARY_SENSORS, id="binary_sensor"),
        pytest.param(RPC_BUTTONS, id="button"),
        pytest.param(RPC_CAMERA_ENTITIES, id="camera"),
        pytest.param(RPC_LINKEDGO_THERMOSTAT, id="climate"),
        pytest.param(RPC_COVERS, id="cover"),
        pytest.param(RPC_FANS, id="fan"),
        pytest.param(RPC_INFRARED_ENTITIES, id="infrared"),
        pytest.param(LIGHTS, id="light"),
        pytest.param(RPC_MEDIA_PLAYER_ENTITIES, id="media_player"),
        pytest.param(RPC_NUMBERS, id="number"),
        pytest.param(RPC_SELECT_ENTITIES, id="select"),
        pytest.param(RPC_SENSORS, id="sensor"),
        pytest.param(RPC_SWITCHES, id="switch"),
        pytest.param(RPC_TEXT_ENTITIES, id="text"),
        pytest.param(RPC_UPDATES, id="update"),
        pytest.param(RPC_VALVES, id="valve"),
    ],
)
def test_rpc_description_attributes_are_unique(
    descriptions: tuple[RpcEntityDescription, ...],
) -> None:
    """Test the keys and legacy IDs of a platform's RPC descriptions are unique."""
    by_attribute = get_rpc_descriptions_by_attribute(descriptions)

    assert all(
        by_attribute[description.key] is description for description in descriptions
    )


@pytest.mark.parametrize(
    "descriptions",
    [
        pytest.param(
            (
                RpcEntityDescription(key="power", components=("switch",)),
                RpcEntityDescription(key="power", components=("light",)),
            ),
            id="key",
        ),
        pytest.param(
            (
                RpcEntityDescription(key="power", components=("switch",)),
                RpcEntityDescription(
                    key="power_pm1",
                    components=("pm1", "light"),
                    legacy_ids={"light": "power"},
                ),
            ),
            id="legacy_id",
        ),
    ],
)
def test_rpc_description_duplicate_attribute(
    descriptions: tuple[RpcEntityDescription, ...],
) -> None:
    """Test a key or legacy ID used by two RPC descriptions is rejected."""
    with pytest.raises(ValueError, match="Duplicate RPC description attribute: power"):
        get_rpc_descriptions_by_attribute(descriptions)
