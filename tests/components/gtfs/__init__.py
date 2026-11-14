"""Tests for the GTFS integration."""

import io
from pathlib import Path
from typing import Any
import zipfile

from universalassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "feed"


def build_feed_zip() -> bytes:
    """Zip the fixture feed."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for path in sorted(FIXTURE_DIR.glob("*.txt")):
            archive.write(path, path.name)
    return buffer.getvalue()


async def setup_yaml_sensor(hass: __HAC_KEEP__, **config: Any) -> None:
    """Set up one legacy YAML GTFS sensor reading feed.zip."""
    assert await async_setup_component(
        hass,
        SENSOR_DOMAIN,
        {SENSOR_DOMAIN: {"platform": "gtfs", "data": "feed.zip", **config}},
    )
    await hass.async_block_till_done()
