"""Configure and test MatrixBot."""

from universalassistant.components.matrix import MatrixBot
from universalassistant.components.matrix.const import DOMAIN, MatrixService
from universalassistant.components.notify import DOMAIN as NOTIFY_DOMAIN
from universalassistant.core import UniversalAssistant

from .conftest import TEST_NOTIFIER_NAME


async def test_services(hass: UniversalAssistant, matrix_bot: MatrixBot) -> None:
    """Test hass/MatrixBot state."""

    services = hass.services.async_services()

    # Verify that the matrix service is registered
    assert (matrix_service := services.get(DOMAIN))
    assert MatrixService.SEND_MESSAGE in matrix_service
    assert MatrixService.REACT in matrix_service

    # Verify that the matrix notifier is registered
    assert (notify_service := services.get(NOTIFY_DOMAIN))
    assert TEST_NOTIFIER_NAME in notify_service
