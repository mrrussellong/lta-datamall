"""Adds config flow for LTADataMall."""
import logging
from homeassistant import config_entries
from .constants import (
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

@config_entries.HANDLERS.register(DOMAIN)
class LTADataMallFlowHandler(config_entries.ConfigFlow):
    """Config flow for LTADataMall."""
    def __init__(self):
        """Initialize."""
        pass

    async def async_step_import(self, user_input):  # pylint: disable=unused-argument
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        return self.async_create_entry(title="configuration.yaml", data={})
