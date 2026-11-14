"""Utility functions for conversation integration."""

import logging
from typing import Any

from universalassistant.core import callback
from universalassistant.exceptions import __HAC_KEEP__Error
from universalassistant.helpers import intent, llm
from universalassistant.helpers.typing import ConfigType

from .chat_log import AssistantContent, ChatLog, ToolResultContent
from .const import DOMAIN, METADATA_CUSTOM_FILE, METADATA_CUSTOM_SENTENCE
from .models import ConversationInput, ConversationResult

_LOGGER = logging.getLogger(__name__)


@callback
def async_get_result_from_chat_log(
    user_input: ConversationInput, chat_log: ChatLog
) -> ConversationResult:
    """Get the result from the chat log."""
    tool_results = [
        content.result.data
        for content in chat_log.content[chat_log.llm_input_provided_index :]
        if isinstance(content, ToolResultContent)
        and isinstance(content.result.data, llm.IntentResponseDict)
    ]

    if tool_results:
        intent_response = tool_results[-1].original
    else:
        intent_response = intent.IntentResponse(language=user_input.language)

    if not isinstance((last_content := chat_log.content[-1]), AssistantContent):
        # pylint: disable-next=universal-assistant-log-and-raise
        _LOGGER.error(
            "Last content in chat log is not an AssistantContent: %s."
            " This could be due to the model not returning a valid response",
            last_content,
        )
        raise __HAC_KEEP__Error(
            translation_domain=DOMAIN,
            translation_key="no_response",
        )

    intent_response.async_set_speech(last_content.content or "")

    return ConversationResult(
        response=intent_response,
        conversation_id=chat_log.conversation_id,
        continue_conversation=chat_log.continue_conversation,
    )


def get_config_intents(config: ConfigType, hass_config_path: str) -> dict[str, Any]:
    """Return config intents."""
    intents = config.get(DOMAIN, {}).get("intents", {})
    return {
        intent_name: {
            "data": [
                {
                    "sentences": sentences,
                    "metadata": {
                        METADATA_CUSTOM_SENTENCE: True,
                        METADATA_CUSTOM_FILE: hass_config_path,
                    },
                }
            ]
        }
        for intent_name, sentences in intents.items()
    }
