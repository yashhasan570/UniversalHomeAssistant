"""Expose images as media sources."""

import math
from pathlib import Path
from time import time

from universalassistant.components.media_source import local_source
from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers.singleton import singleton

from .const import DATA_MEDIA_SOURCE, DOMAIN, IMAGE_DIR, LOGGER


@singleton(DATA_MEDIA_SOURCE, async_=True)
async def async_get_media_source(hass: __HAC_KEEP__) -> local_source.LocalSource:
    """Set up local media source."""
    media_dirs = list(hass.config.media_dirs.values())

    if not media_dirs:
        raise __HAC_KEEP__Error(
            "AI Task media source requires at least one media directory configured"
        )

    media_dir = Path(media_dirs[0]) / DOMAIN / IMAGE_DIR

    return local_source.LocalSource(
        hass,
        DOMAIN,
        "AI generated images",
        {IMAGE_DIR: str(media_dir)},
        f"/{DOMAIN}",
    )


async def async_clear_images(hass: __HAC_KEEP__, days: int | None) -> None:
    """Delete generated images, or only those older than the given days."""
    source = await async_get_media_source(hass)
    image_dir = Path(source.media_dirs[IMAGE_DIR])
    cutoff = time() - days * 86400 if days else math.inf

    def remove_images() -> None:
        """Remove images from the filesystem."""
        if not image_dir.is_dir():
            return
        for image in image_dir.iterdir():
            try:
                if not image.is_file() or image.stat().st_mtime >= cutoff:
                    continue
                image.unlink()
            except OSError as err:
                LOGGER.warning("Can't remove image '%s': %s", image.name, err)

    await hass.async_add_executor_job(remove_images)
