"""Test cryptographic hash functions for __HA_KEEP__ templates."""

from universalassistant.core import __HAC_KEEP__

from tests.helpers.template.helpers import render


def test_md5(hass: __HAC_KEEP__) -> None:
    """Test the md5 function and filter."""
    ha_md5 = "3d15e5c102c3413d0337393c3287e006"
    assert render(hass, "{{ md5('__HA_KEEP__') }}") == ha_md5
    assert render(hass, "{{ '__HA_KEEP__' | md5 }}") == ha_md5


def test_sha1(hass: __HAC_KEEP__) -> None:
    """Test the sha1 function and filter."""
    ha_sha1 = "c8fd3bb19b94312664faa619af7729bdbf6e9f8a"
    assert render(hass, "{{ sha1('__HA_KEEP__') }}") == ha_sha1
    assert render(hass, "{{ '__HA_KEEP__' | sha1 }}") == ha_sha1


def test_sha256(hass: __HAC_KEEP__) -> None:
    """Test the sha256 function and filter."""
    ha_sha256 = "2a366abb0cd47f51f3725bf0fb7ebcb4fefa6e20f4971e25fe2bb8da8145ce2b"
    assert render(hass, "{{ sha256('__HA_KEEP__') }}") == ha_sha256
    assert render(hass, "{{ '__HA_KEEP__' | sha256 }}") == ha_sha256


def test_sha512(hass: __HAC_KEEP__) -> None:
    """Test the sha512 function and filter."""
    ha_sha512 = (
        "9e3c2cdd1fbab0037378d37e1baf8a3a4bf92c54b56ad1d459deee30"
        "ccbb2acbebd7a3614552ea08992ad27dedeb7b4c5473525ba90cb73d"
        "be8b9ec5f69295bb"
    )
    assert render(hass, "{{ sha512('__HA_KEEP__') }}") == ha_sha512
    assert render(hass, "{{ '__HA_KEEP__' | sha512 }}") == ha_sha512
