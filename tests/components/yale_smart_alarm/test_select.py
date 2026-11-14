"""The test for the Yale smart living select."""

from unittest.mock import Mock

import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion
from yalesmartalarmclient import YaleSmartAlarmData

from universalassistant.components.select import (
    DOMAIN as SELECT_DOMAIN,
    SelectService,
    SelectServiceArgument,
)
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import ServiceValidationError
from universalassistant.helpers import entity_registry as er


@pytest.mark.parametrize(
    "load_platforms",
    [[Platform.SELECT]],
)
async def test_switch(
    hass: UniversalAssistant,
    entity_registry: er.EntityRegistry,
    load_config_entry: tuple[MockConfigEntry, Mock],
    get_data: YaleSmartAlarmData,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the Yale Smart Living volume select."""
    client = load_config_entry[1]

    await snapshot_platform(
        hass, entity_registry, snapshot, load_config_entry[0].entry_id
    )

    await hass.services.async_call(
        SELECT_DOMAIN,
        SelectService.SELECT_OPTION,
        {
            CommonServiceArgument.ENTITY_ID: "select.device1_volume",
            SelectServiceArgument.OPTION: "high",
        },
        blocking=True,
    )

    client.auth.post_authenticated.assert_called_once()
    client.auth.put_authenticated.assert_called_once()

    state = hass.states.get("select.device1_volume")
    assert state.state == "high"

    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(
            SELECT_DOMAIN,
            SelectService.SELECT_OPTION,
            {
                CommonServiceArgument.ENTITY_ID: "select.device1_volume",
                SelectServiceArgument.OPTION: "not_exist",
            },
            blocking=True,
        )
