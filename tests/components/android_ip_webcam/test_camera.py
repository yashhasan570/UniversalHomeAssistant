"""Test the Android IP Webcam camera."""

from typing import Any

import pytest
from pytest_universalassistant.common import MockConfigEntry

from universalassistant.components.android_ip_webcam.const import DOMAIN
from universalassistant.components.camera import async_get_stream_source
from universalassistant.core import __HAC_KEEP__


@pytest.mark.usefixtures("aioclient_mock_fixture")
@pytest.mark.parametrize(
    ("config", "expected_stream_source"),
    [
        (
            {
                "host": "1.1.1.1",
                "port": 8080,
                "username": "user",
                "password": "pass",
            },
            "rtsp://user:pass@1.1.1.1:8080/h264_aac.sdp",
        ),
        (
            {
                "host": "1.1.1.1",
                "port": 8080,
            },
            "rtsp://1.1.1.1:8080/h264_aac.sdp",
        ),
    ],
)
async def test_camera_stream_source(
    hass: __HAC_KEEP__,
    config: dict[str, Any],
    expected_stream_source: str,
) -> None:
    """Test camera stream source."""
    entity_id = "camera.1_1_1_1"
    entry = MockConfigEntry(domain=DOMAIN, data=config)
    entry.add_to_hass(hass)

    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    state = hass.states.get(entity_id)
    assert state is not None

    stream_source = await async_get_stream_source(hass, entity_id)

    assert stream_source == expected_stream_source
