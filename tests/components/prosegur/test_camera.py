"""The camera tests for the prosegur platform."""

from unittest.mock import AsyncMock, MagicMock

from pyprosegur.exceptions import ProsegurException
import pytest

from universalassistant.components import camera
from universalassistant.components.camera import Image
from universalassistant.components.prosegur.const import DOMAIN
from universalassistant.const import ATTR_ENTITY_ID
from universalassistant.core import UniversalAssistant
from universalassistant.exceptions import UniversalAssistantError


async def test_camera(hass: UniversalAssistant, init_integration) -> None:
    """Test prosegur get_image."""

    image = await camera.async_get_image(hass, "camera.contract_1234abcd_test_cam")

    assert image == Image(content_type="image/jpeg", content=b"ABC")


@pytest.mark.usefixtures("init_integration")
async def test_camera_fail(hass: UniversalAssistant, mock_install: MagicMock) -> None:
    """Test prosegur get_image fails."""

    mock_install.get_image = AsyncMock(side_effect=ProsegurException())

    with pytest.raises(
        UniversalAssistantError, match="Unable to get image from camera test_cam"
    ):
        await camera.async_get_image(hass, "camera.contract_1234abcd_test_cam")


async def test_request_image(
    hass: UniversalAssistant, init_integration, mock_install
) -> None:
    """Test the camera request image service."""

    await hass.services.async_call(
        DOMAIN,
        "request_image",
        {ATTR_ENTITY_ID: "camera.contract_1234abcd_test_cam"},
    )
    await hass.async_block_till_done()

    assert mock_install.request_image.called


@pytest.mark.usefixtures("init_integration")
async def test_request_image_fail(hass: UniversalAssistant, mock_install: MagicMock) -> None:
    """Test the camera request image service fails."""

    mock_install.request_image = AsyncMock(side_effect=ProsegurException())

    with pytest.raises(
        UniversalAssistantError,
        match="Unable to request a new image from camera test_cam",
    ):
        await hass.services.async_call(
            DOMAIN,
            "request_image",
            {ATTR_ENTITY_ID: "camera.contract_1234abcd_test_cam"},
            blocking=True,
        )

    assert mock_install.request_image.called
