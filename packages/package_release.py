"""Pin pytest-universalassistant to the Universal Universal Home Assistant release being published."""

from pathlib import Path
import tomllib

PACKAGE_PATH = Path("packages/pytest-universalassistant/pyproject.toml")


def main() -> None:
    """Set the package version and pin the matching universalassistant release."""
    version = tomllib.loads(Path("pyproject.toml").read_text())["project"]["version"]
    content = PACKAGE_PATH.read_text()
    for old, new in (
        ('version = "0.0.0"', f'version = "{version}"'),
        ('"universalassistant",', f'"universalassistant=={version}",'),
    ):
        if content.count(old) != 1:
            raise SystemExit(f"Expected exactly one {old} in {PACKAGE_PATH}")
        content = content.replace(old, new)
    PACKAGE_PATH.write_text(content)


if __name__ == "__main__":
    main()
