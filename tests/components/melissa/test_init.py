"""The test for the Melissa Climate component."""

from universalassistant.core import UniversalAssistant

from . import setup_integration


async def test_setup(hass: UniversalAssistant, mock_melissa) -> None:
    """Test setting up the Melissa component."""
    await setup_integration(hass)

    mock_melissa.assert_called_with(username="********", password="********")
