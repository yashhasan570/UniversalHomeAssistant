"""Test the __HA_KEEP__ package init."""

import subprocess
import sys

import httpcore2
import httpx2
import pytest

IMPORT_TIMEOUT = 60


def test_probatio_codecs_is_imported_before_the_event_loop() -> None:
    """Importing __HA_KEEP__ must leave no lazy codec import for the loop.

    Probatio resolves to_field_list and to_openapi through a lazy import of
    probatio.codecs on first attribute access, and both are reached from the
    event loop: the first renders every config flow form, the second builds the
    tool schemas for a conversation turn.

    A clean interpreter is the only way to see this: anything the test suite
    imported first would hide it.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys, universalassistant; print('probatio.codecs' in sys.modules)",
        ],
        capture_output=True,
        check=True,
        text=True,
        timeout=IMPORT_TIMEOUT,
    )

    assert result.stdout.strip() == "True"


def test_httpx_is_aliased_to_httpx2() -> None:
    """Test httpx and httpcore resolve to httpx2 and httpcore2."""
    import httpcore  # noqa: PLC0415
    import httpx  # noqa: PLC0415
    from httpx._exceptions import HTTPError  # noqa: PLC0415

    assert httpx is httpx2
    assert httpcore is httpcore2
    assert HTTPError is httpx2.HTTPError


@pytest.mark.parametrize("module", ["httpx", "httpcore"])
def test_early_httpx_import_fails_loudly(module: str) -> None:
    """Test importing httpx before __HA_KEEP__ fails instead of splitting classes.

    A clean interpreter is needed, as the test suite already imported Home
    Assistant.
    """
    result = subprocess.run(
        [sys.executable, "-c", f"import {module}, universalassistant"],
        capture_output=True,
        check=False,
        text=True,
        timeout=IMPORT_TIMEOUT,
    )

    assert result.returncode != 0
    assert f"{module} was already imported" in result.stderr
