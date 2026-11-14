"""Test version functions for __HA_KEEP__ templates."""

import pytest

from universalassistant.core import __HAC_KEEP__
from universalassistant.exceptions import TemplateError

from tests.helpers.template.helpers import render


def test_version(hass: __HAC_KEEP__) -> None:
    """Test version filter and function."""
    filter_result = render(hass, "{{ '2099.9.9' | version}}")
    function_result = render(hass, "{{ version('2099.9.9')}}")
    assert filter_result == function_result == "2099.9.9"

    filter_result = render(hass, "{{ '2099.9.9' | version < '2099.9.10' }}")
    function_result = render(hass, "{{ version('2099.9.9') < '2099.9.10' }}")
    assert filter_result is function_result is True

    filter_result = render(hass, "{{ '2099.9.9' | version == '2099.9.9' }}")
    function_result = render(hass, "{{ version('2099.9.9') == '2099.9.9' }}")
    assert filter_result is function_result is True

    with pytest.raises(TemplateError):
        render(hass, "{{ version(None) < '2099.9.10' }}")
