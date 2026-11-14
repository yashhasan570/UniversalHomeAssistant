"""Tests for ZoneMinder YAML configuration validation."""

from universalassistant.components.zoneminder.const import DOMAIN
from universalassistant.const import CONF_HOST, CONF_SSL
from universalassistant.core import __HAC_KEEP__
from universalassistant.setup import async_setup_component

from .conftest import MOCK_HOST


async def test_invalid_config_missing_host(hass: __HAC_KEEP__) -> None:
    """Test that config without host is rejected."""
    config: dict = {DOMAIN: [{}]}

    result = await async_setup_component(hass, DOMAIN, config)
    assert not result


async def test_invalid_config_bad_ssl_type(hass: __HAC_KEEP__) -> None:
    """Test that non-boolean ssl value is rejected."""
    config = {DOMAIN: [{CONF_HOST: MOCK_HOST, CONF_SSL: "not_bool"}]}

    result = await async_setup_component(hass, DOMAIN, config)
    assert not result
