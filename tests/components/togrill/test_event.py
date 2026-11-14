"""Test events for ToGrill integration."""

from unittest.mock import Mock

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from pytest_universalassistant.components.bluetooth import inject_bluetooth_service_info
from syrupy.assertion import SnapshotAssertion
from togrill_bluetooth.packets import PacketA1Notify, PacketA5Notify

from universalassistant.components.event import EventEntityStateAttribute
from universalassistant.const import STATE_UNKNOWN, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.helpers import entity_registry as er
from universalassistant.util import slugify

from . import TOGRILL_SERVICE_INFO, setup_entry


@pytest.mark.freeze_time("2023-10-21")
@pytest.mark.parametrize(
    "packets",
    [
        pytest.param([], id="no_data"),
        pytest.param([PacketA1Notify([10, None])], id="non_event_packet"),
        pytest.param([PacketA5Notify(probe=1, message=99)], id="non_known_message"),
    ],
)
async def test_setup(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_entry: MockConfigEntry,
    mock_client: Mock,
    packets,
) -> None:
    """Test standard events."""

    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO)

    await setup_entry(hass, mock_entry, [Platform.EVENT])

    for packet in packets:
        mock_client.mocked_notify(packet)

    await snapshot_platform(hass, entity_registry, snapshot, mock_entry.entry_id)


@pytest.mark.freeze_time("2023-10-21")
@pytest.mark.parametrize(
    "message",
    [pytest.param(message, id=message.name) for message in PacketA5Notify.Message],
)
async def test_events(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_entry: MockConfigEntry,
    mock_client: Mock,
    message: PacketA5Notify.Message,
) -> None:
    """Test all possible events."""

    inject_bluetooth_service_info(hass, TOGRILL_SERVICE_INFO)

    await setup_entry(hass, mock_entry, [Platform.EVENT])

    mock_client.mocked_notify(PacketA5Notify(probe=1, message=message))

    state = hass.states.get("event.pro_05_probe_2_event")
    assert state
    assert state.state == STATE_UNKNOWN

    state = hass.states.get("event.pro_05_probe_1_event")
    assert state
    assert state.state == "2023-10-21T00:00:00.000+00:00"
    assert state.attributes.get(EventEntityStateAttribute.EVENT_TYPE) == slugify(
        message.name
    )
