"""Constants for the OpenRouter integration."""

import logging

from universalassistant.const import CONF_LLM_HASS_API, CONF_PROMPT
from universalassistant.helpers import llm

DOMAIN = "open_router"
LOGGER = logging.getLogger(__package__)

CONF_RECOMMENDED = "recommended"
CONF_WEB_SEARCH = "web_search"
CONF_OUTPUT_MODALITIES = "output_modalities"
CONF_REASONING = "reasoning"

RECOMMENDED_WEB_SEARCH = "off"
RECOMMENDED_REASONING = "auto"

RECOMMENDED_CONVERSATION_OPTIONS = {
    CONF_RECOMMENDED: True,
    CONF_LLM_HASS_API: [llm.LLM_API_ASSIST],
    CONF_PROMPT: llm.DEFAULT_INSTRUCTIONS_PROMPT,
    CONF_WEB_SEARCH: RECOMMENDED_WEB_SEARCH,
    CONF_REASONING: RECOMMENDED_REASONING,
}
