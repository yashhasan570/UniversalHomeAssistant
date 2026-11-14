"""The test for the version sensor platform."""

from freezegun.api import FrozenDateTimeFactory
from pyhaversion.exceptions import HaVersionException
import pytest

from universalassistant.core import UniversalAssistant

from .common import MOCK_VERSION, mock_get_version_update, setup_version_integration


async def test_version_sensor(hass: UniversalAssistant) -> None:
    """Test the Version sensor with different sources."""
    await setup_version_integration(hass)

    state = hass.states.get("sensor.universal_assistant_version_local_installation")
    assert state.state == MOCK_VERSION
    assert "source" not in state.attributes
    assert "channel" not in state.attributes


async def test_update(
    hass: UniversalAssistant,
    caplog: pytest.LogCaptureFixture,
    freezer: FrozenDateTimeFactory,
) -> None:
    """Test updates."""
    await setup_version_integration(hass)
    assert (
        hass.states.get("sensor.universal_assistant_version_local_installation").state
        == MOCK_VERSION
    )

    await mock_get_version_update(hass, freezer, version="1970.1.1")
    assert (
        hass.states.get("sensor.universal_assistant_version_local_installation").state
        == "1970.1.1"
    )

    assert "Error fetching version data" not in caplog.text
    await mock_get_version_update(hass, freezer, side_effect=HaVersionException)
    assert (
        hass.states.get("sensor.universal_assistant_version_local_installation").state
        == "unavailable"
    )
    assert "Error fetching version data" in caplog.text
