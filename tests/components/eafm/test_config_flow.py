"""Tests for eafm config flow."""

from unittest.mock import patch

from probatio.error import Invalid
import pytest

from universalassistant import config_entries
from universalassistant.components.eafm import const
from universalassistant.core import __HAC_KEEP__
from universalassistant.data_entry_flow import FlowResultType


async def test_flow_no_discovered_stations(
    hass: __HAC_KEEP__, mock_get_stations
) -> None:
    """Test config flow discovers no station."""
    mock_get_stations.return_value = []
    result = await hass.config_entries.flow.async_init(
        const.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "no_stations"


async def test_flow_invalid_station(hass: __HAC_KEEP__, mock_get_stations) -> None:
    """Test config flow errors on invalid station."""
    mock_get_stations.return_value = [
        {"label": "My station", "stationReference": "L12345", "RLOIid": "R12345"}
    ]

    result = await hass.config_entries.flow.async_init(
        const.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    with pytest.raises(Invalid):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={"station": "My other station"}
        )


async def test_flow_works(
    hass: __HAC_KEEP__, mock_get_stations, mock_get_station
) -> None:
    """Test config flow discovers no station."""
    mock_get_stations.return_value = [
        {"label": "My station", "stationReference": "L12345", "RLOIid": "R12345"}
    ]
    mock_get_station.return_value = [
        {"label": "My station", "stationReference": "L12345", "RLOIid": "R12345"}
    ]

    result = await hass.config_entries.flow.async_init(
        const.DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM

    with patch("universalassistant.components.eafm.async_setup_entry", return_value=None):
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={"station": "My station - R12345"}
        )

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "My station - R12345"
    assert result["data"] == {
        "station": "L12345",
    }
    assert result["result"].unique_id == "L12345"
