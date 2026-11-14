"""Test the Agent DVR alarm control panel."""

import pytest
from pytest_universalassistant.common import async_load_json_object_fixture
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker

from universalassistant.components.agent_dvr.const import DOMAIN
from universalassistant.components.alarm_control_panel import AlarmControlPanelState
from universalassistant.const import CONTENT_TYPE_JSON
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers.entity_component import async_update_entity

from . import init_integration

ENTITY_ID = "alarm_control_panel.desktop_alarm_panel"


@pytest.mark.parametrize(
    ("profiles", "expected"),
    [
        ([{"name": "Home", "active": True}], AlarmControlPanelState.ARMED_HOME),
        ([{"name": "Night", "active": True}], AlarmControlPanelState.ARMED_NIGHT),
        ([{"name": "Away", "active": True}], AlarmControlPanelState.ARMED_AWAY),
        ([{"name": "Home", "active": False}], AlarmControlPanelState.ARMED_AWAY),
    ],
    ids=["home", "night", "away", "no_active_profile"],
)
async def test_armed_state(
    hass: __HAC_KEEP__,
    aioclient_mock: AiohttpClientMocker,
    profiles: list[dict],
    expected: AlarmControlPanelState,
) -> None:
    """Test the armed state follows the active profile, if there is one."""
    await init_integration(hass, aioclient_mock)

    status = await async_load_json_object_fixture(hass, "status.json", DOMAIN)
    status["armed"] = True
    aioclient_mock.clear_requests()
    aioclient_mock.get(
        "http://example.local:8090/command.cgi?cmd=getStatus",
        json=status,
        headers={"Content-Type": CONTENT_TYPE_JSON},
    )
    aioclient_mock.get(
        "http://example.local:8090/command.cgi?cmd=getProfiles",
        json={"profiles": profiles},
        headers={"Content-Type": CONTENT_TYPE_JSON},
    )

    await async_update_entity(hass, ENTITY_ID)

    assert hass.states.get(ENTITY_ID).state == expected
