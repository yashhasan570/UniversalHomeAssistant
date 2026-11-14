"""Test Home Connect application credentials."""

import pytest

from universalassistant.components.home_connect.application_credentials import (
    async_get_description_placeholders,
)
from universalassistant.core import UniversalAssistant


@pytest.mark.parametrize(
    ("country", "domain"),
    [
        pytest.param("CN", "developer.home-connect.cn", id="china"),
        pytest.param("ES", "developer.home-connect.com", id="spain"),
        pytest.param(None, "developer.home-connect.com", id="no_country"),
    ],
)
async def test_description_placeholders(
    hass: UniversalAssistant, country: str | None, domain: str
) -> None:
    """Test description placeholders use the region specific developer portal."""
    hass.config.country = country
    assert await async_get_description_placeholders(hass) == {
        "developer_dashboard_url": f"https://{domain}/",
        "applications_url": f"https://{domain}/applications",
        "register_application_url": f"https://{domain}/application/add",
        "redirect_url": "https://my.universalassistant.io/redirect/oauth",
    }
