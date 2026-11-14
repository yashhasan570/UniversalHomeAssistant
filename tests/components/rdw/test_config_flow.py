"""Tests for the RDW config flow."""

from unittest.mock import MagicMock

import pytest
from pytest_universalassistant.common import MockConfigEntry
from vehicle.exceptions import RDWConnectionError, RDWUnknownLicensePlateError

from universalassistant.components.rdw.const import CONF_LICENSE_PLATE, DOMAIN
from universalassistant.config_entries import SOURCE_USER
from universalassistant.core import UniversalAssistant
from universalassistant.data_entry_flow import FlowResultType

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


@pytest.mark.usefixtures("mock_rdw")
async def test_full_user_flow(hass: UniversalAssistant) -> None:
    """Test the full user configuration flow."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_LICENSE_PLATE: "11-ZKZ-3"},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "11-ZKZ-3"
    assert result["data"] == {CONF_LICENSE_PLATE: "11ZKZ3"}
    assert result["result"].unique_id == "11ZKZ3"


@pytest.mark.parametrize(
    ("side_effect", "expected_error"),
    [
        (RDWUnknownLicensePlateError, {"base": "unknown_license_plate"}),
        (RDWConnectionError, {"base": "cannot_connect"}),
    ],
)
async def test_user_flow_errors(
    hass: UniversalAssistant,
    mock_rdw: MagicMock,
    side_effect: type[Exception],
    expected_error: dict[str, str],
) -> None:
    """Test the user flow with errors and recovery."""
    mock_rdw.vehicle.side_effect = side_effect

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_LICENSE_PLATE: "0001TJ"},
    )

    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == expected_error

    mock_rdw.vehicle.side_effect = None

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_LICENSE_PLATE: "11-ZKZ-3"},
    )

    assert result["type"] is FlowResultType.CREATE_ENTRY


@pytest.mark.usefixtures("mock_rdw")
async def test_user_flow_already_configured(
    hass: UniversalAssistant,
    mock_config_entry: MockConfigEntry,
) -> None:
    """Test the user flow when the vehicle is already configured."""
    mock_config_entry.add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": SOURCE_USER}
    )

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        user_input={CONF_LICENSE_PLATE: "11-ZKZ-3"},
    )

    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
