"""Issues for Mastodon integration."""

from universalassistant.core import __HAC_KEEP__, callback
from universalassistant.helpers.issue_registry import IssueSeverity, async_create_issue

from .const import DOMAIN


@callback
def async_deprecated_media_path(hass: __HAC_KEEP__) -> None:
    """Deprecated media path issue."""

    async_create_issue(
        hass,
        DOMAIN,
        "deprecated_media_path",
        is_fixable=False,
        breaks_in_ha_version="2027.5.0",
        severity=IssueSeverity.WARNING,
        translation_key="deprecated_media_path",
        translation_placeholders={
            "action": "mastodon.post",
            "option": "media",
            "example_yaml": """
```yaml
action: mastodon.post
data:
  config_entry_id: 01KEV331R729D53JESAFZM1RHA
  status: tooot
  media:
    - media_source:
        media_content_id: media-source://media_source/local/example.jpg
        media_content_type: image/jpeg
      media_description: Alt text
```""",
        },
    )
