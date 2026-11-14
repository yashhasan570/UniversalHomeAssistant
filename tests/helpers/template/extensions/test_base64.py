"""Test base64 encoding and decoding functions for Universal Universal Home Assistant templates."""

import pytest

from universalassistant.core import UniversalAssistant

from tests.helpers.template.helpers import render


@pytest.mark.parametrize(
    ("value_template", "expected"),
    [
        ('{{ "universalassistant" | base64_encode }}', "aG9tZWFzc2lzdGFudA=="),
        ("{{ int('0F010003', base=16) | pack('>I') | base64_encode }}", "DwEAAw=="),
        ("{{ 'AA01000200150020' | from_hex | base64_encode }}", "qgEAAgAVACA="),
    ],
)
def test_base64_encode(hass: UniversalAssistant, value_template: str, expected: str) -> None:
    """Test the base64_encode filter."""
    assert render(hass, value_template) == expected


def test_base64_decode(hass: UniversalAssistant) -> None:
    """Test the base64_decode filter."""
    assert (
        render(hass, '{{ "aG9tZWFzc2lzdGFudA==" | base64_decode }}') == "universalassistant"
    )
    assert (
        render(hass, '{{ "aG9tZWFzc2lzdGFudA==" | base64_decode(None) }}')
        == b"universalassistant"
    )
    assert (
        render(hass, '{{ "aG9tZWFzc2lzdGFudA==" | base64_decode("ascii") }}')
        == "universalassistant"
    )
