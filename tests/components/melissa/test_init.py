"""The test for the Melissa Climate component."""

from universalassistant.core import __HAC_KEEP__

from . import setup_integration


async def test_setup(hass: __HAC_KEEP__, mock_melissa) -> None:
    """Test setting up the Melissa component."""
    await setup_integration(hass)

    mock_melissa.assert_called_with(username="********", password="********")
