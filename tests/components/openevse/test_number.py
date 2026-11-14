"""Tests for the OpenEVSE number platform."""

from unittest.mock import MagicMock, patch

from aiohttp import ContentTypeError, ServerTimeoutError
from openevsehttp.exceptions import (
    AuthenticationError,
    ParseJSONError,
    UnknownError,
    UnsupportedFeature,
)
import pytest
from pytest_universalassistant.common import MockConfigEntry, snapshot_platform
from syrupy.assertion import SnapshotAssertion

from universalassistant.components.number import (
    DOMAIN as NUMBER_DOMAIN,
    NumberService,
    NumberServiceArgument,
)
from universalassistant.components.openevse.const import DOMAIN
from universalassistant.const import CommonServiceArgument, Platform
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import (
    ConfigEntryAuthFailed,
    __HAC_KEEP__Error,
    ServiceValidationError,
)
from universalassistant.helpers import entity_registry as er


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_entities(
    hass: __HAC_KEEP__,
    entity_registry: er.EntityRegistry,
    snapshot: SnapshotAssertion,
    mock_config_entry: MockConfigEntry,
    mock_charger: MagicMock,
) -> None:
    """Test the sensor entities."""
    with patch("universalassistant.components.openevse.PLATFORMS", [Platform.NUMBER]):
        mock_config_entry.add_to_hass(hass)
        await hass.config_entries.async_setup(mock_config_entry.entry_id)

    await snapshot_platform(hass, entity_registry, snapshot, mock_config_entry.entry_id)


async def test_set_value(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_charger: MagicMock,
) -> None:
    """Test the disabled by default sensor entities."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    await hass.services.async_call(
        NUMBER_DOMAIN,
        NumberService.SET_VALUE,
        {
            CommonServiceArgument.ENTITY_ID: "number.openevse_mock_config_charge_rate",
            NumberServiceArgument.VALUE: 32.0,
        },
        blocking=True,
    )
    mock_charger.set_current.assert_called_once_with(32.0)


@pytest.mark.parametrize(
    ("raised", "expected", "translation_key", "translation_placeholders"),
    [
        pytest.param(
            ValueError("out of range"),
            ServiceValidationError,
            "invalid_value",
            {"value": "32.0"},
            id="value_error",
        ),
        pytest.param(
            AuthenticationError("bad creds"),
            ConfigEntryAuthFailed,
            "authentication_error",
            None,
            id="auth_error",
        ),
        pytest.param(
            TimeoutError("timed out"),
            __HAC_KEEP__Error,
            "communication_error",
            None,
            id="timeout_error",
        ),
        pytest.param(
            ServerTimeoutError("timed out"),
            __HAC_KEEP__Error,
            "communication_error",
            None,
            id="server_timeout_error",
        ),
        pytest.param(
            ParseJSONError("bad json"),
            __HAC_KEEP__Error,
            "communication_error",
            None,
            id="parse_json_error",
        ),
        pytest.param(
            UnsupportedFeature("old firmware"),
            __HAC_KEEP__Error,
            "unsupported_feature",
            None,
            id="unsupported_feature",
        ),
        pytest.param(
            ContentTypeError(MagicMock(), (), message="bad content"),
            __HAC_KEEP__Error,
            "communication_error",
            None,
            id="content_type_error",
        ),
        pytest.param(
            UnknownError("unknown error"),
            __HAC_KEEP__Error,
            "communication_error",
            None,
            id="unknown_error",
        ),
        pytest.param(
            RuntimeError("runtime error"),
            __HAC_KEEP__Error,
            "communication_error",
            None,
            id="runtime_error",
        ),
    ],
)
async def test_set_value_raises(
    hass: __HAC_KEEP__,
    mock_config_entry: MockConfigEntry,
    mock_charger: MagicMock,
    raised: Exception,
    expected: type[Exception],
    translation_key: str,
    translation_placeholders: dict[str, str] | None,
) -> None:
    """Test that errors from the charger are translated to HA exceptions."""
    mock_config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    mock_charger.set_current.side_effect = raised

    with pytest.raises(expected) as exc_info:
        await hass.services.async_call(
            NUMBER_DOMAIN,
            NumberService.SET_VALUE,
            {
                CommonServiceArgument.ENTITY_ID: "number.openevse_mock_config_charge_rate",
                NumberServiceArgument.VALUE: 32.0,
            },
            blocking=True,
        )

    assert exc_info.value.translation_key == translation_key
    assert exc_info.value.translation_domain == DOMAIN
    assert exc_info.value.translation_placeholders == translation_placeholders
