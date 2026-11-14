"""Test VoIP select."""

from universalassistant.components.voip.devices import VoIPDevice
from universalassistant.config_entries import ConfigEntry
from universalassistant.core import __HAC_KEEP__


async def test_pipeline_select(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    voip_device: VoIPDevice,
) -> None:
    """Test pipeline select.

    Functionality is tested in assist_pipeline/test_select.py.
    This test is only to ensure it is set up.
    """
    state = hass.states.get("select.192_168_1_210_assistant")
    assert state is not None
    assert state.state == "preferred"


async def test_vad_sensitivity_select(
    hass: __HAC_KEEP__,
    config_entry: ConfigEntry,
    voip_device: VoIPDevice,
) -> None:
    """Test VAD sensitivity select.

    Functionality is tested in assist_pipeline/test_select.py.
    This test is only to ensure it is set up.
    """
    state = hass.states.get("select.192_168_1_210_finished_speaking_detection")
    assert state is not None
    assert state.state == "default"
