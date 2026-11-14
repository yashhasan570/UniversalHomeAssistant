"""nuki integration helpers."""

from universalassistant import exceptions


def parse_id(hardware_id):
    """Parse Nuki ID."""
    return hex(hardware_id).split("x")[-1].upper()


class CannotConnect(exceptions.__HAC_KEEP__Error):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.__HAC_KEEP__Error):
    """Error to indicate there is invalid auth."""


class NukiWebhookException(exceptions.__HAC_KEEP__Error):
    """Error to indicate there was an issue with the webhook."""
