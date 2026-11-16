"""group conftest."""

import pytest

from universalassistant.core import UniversalAssistant
from universalassistant.setup import async_setup_component

from tests.components.light.conftest import mock_light_profiles  # noqa: F401


@pytest.fixture(autouse=True)
async def setup_universalassistant(hass: UniversalAssistant):
    """Set up the universalassistant integration."""
    await async_setup_component(hass, "universalassistant", {})
