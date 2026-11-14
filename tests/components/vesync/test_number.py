"""Tests for the number platform."""

from unittest.mock import patch

import pytest
from pytest_universalassistant.common import MockConfigEntry
from pytest_universalassistant.test_util.aiohttp import AiohttpClientMocker
from pyvesync.devices.vesynchumidifier import VeSyncHumid200300S
from pyvesync.utils.errors import ResponseInfo

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.const import CommonServiceArgument
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error, ServiceValidationError
from universalassistant.helpers import entity_registry as er

from .common import (
    ALL_DEVICE_NAMES,
    ENTITY_HUMIDIFIER_MIST_LEVEL,
    mock_devices_response,
)

NON_HUMIDIFIER_DEVICE_NAMES = [
    name for name in ALL_DEVICE_NAMES if not name.startswith("Humidifier")
]


async def test_set_mist_level_bad_range(
    hass: __HAC_KEEP__, humidifier_config_entry: MockConfigEntry
) -> None:
    """Test set_mist_level invalid value."""
    with (
        pytest.raises(ServiceValidationError),
        patch(
            "pyvesync.devices.vesynchumidifier.VeSyncHumid200300S.set_mist_level",
            return_value=True,
        ) as method_mock,
    ):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: ENTITY_HUMIDIFIER_MIST_LEVEL,
                NumberServiceArgument.VALUE: "10",
            },
            blocking=True,
        )
    await hass.async_block_till_done()
    method_mock.assert_not_called()


async def test_set_mist_level(
    hass: __HAC_KEEP__, humidifier_config_entry: MockConfigEntry
) -> None:
    """Test set_mist_level usage."""

    with patch(
        "pyvesync.devices.vesynchumidifier.VeSyncHumid200300S.set_mist_level",
        return_value=True,
    ) as method_mock:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: ENTITY_HUMIDIFIER_MIST_LEVEL,
                NumberServiceArgument.VALUE: "3",
            },
            blocking=True,
        )
    await hass.async_block_till_done()
    method_mock.assert_called_once()


@pytest.mark.parametrize(
    ("last_response", "message"),
    [
        pytest.param(
            ResponseInfo(name="error", error_type="error", message="Device error"),
            "Device error",
            id="last_response",
        ),
        pytest.param(None, "Failed to set value.", id="no_last_response"),
    ],
)
async def test_set_mist_level_failure(
    hass: __HAC_KEEP__,
    humidifier_config_entry: MockConfigEntry,
    last_response: ResponseInfo | None,
    message: str,
) -> None:
    """Test a failed set_mist_level raises __HAC_KEEP__Error."""

    async def _set_mist_level(device: VeSyncHumid200300S, level: int) -> bool:
        device.last_response = last_response
        return False

    with (
        patch.object(
            VeSyncHumid200300S,
            "set_mist_level",
            autospec=True,
            side_effect=_set_mist_level,
        ),
        pytest.raises(__HAC_KEEP__Error, match=message),
    ):
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: ENTITY_HUMIDIFIER_MIST_LEVEL,
                NumberServiceArgument.VALUE: "3",
            },
            blocking=True,
        )


async def test_mist_level(
    hass: __HAC_KEEP__, humidifier_config_entry: MockConfigEntry
) -> None:
    """Test the state of mist_level number entity."""

    assert hass.states.get(ENTITY_HUMIDIFIER_MIST_LEVEL).state == "6"


@pytest.mark.parametrize("device_name", NON_HUMIDIFIER_DEVICE_NAMES)
async def test_no_number_entities_for_non_humidifiers(
    hass: __HAC_KEEP__,
    config_entry: MockConfigEntry,
    entity_registry: er.EntityRegistry,
    aioclient_mock: AiohttpClientMocker,
    caplog: pytest.LogCaptureFixture,
    device_name: str,
) -> None:
    """Test devices that are not humidifiers get no number entities."""
    mock_devices_response(aioclient_mock, device_name)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # A crashing platform setup would also leave no entities behind.
    assert "Error while setting up vesync platform for number" not in caplog.text
    assert not [
        entity
        for entity in er.async_entries_for_config_entry(
            entity_registry, config_entry.entry_id
        )
        if entity.domain == NUMBER_DOMAIN
    ]
