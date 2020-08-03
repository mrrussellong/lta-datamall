"""Support for LTADataMall domain"""
from .api import LTADataMall
import logging
from homeassistant import config_entries
from homeassistant.const import (
    CONF_SENSORS,
)
from .constants import (
    DOMAIN,
    CONF_ACCOUNT_KEY,
    CONFIG_SCHEMA,
    PLATFORM,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Setup the LTADataMall platform."""
    conf = CONFIG_SCHEMA(config).get(DOMAIN)
    
    hass.data[DOMAIN] = ConnectionPlatform(
        conf.get(CONF_ACCOUNT_KEY),
    )

    if conf.get(CONF_SENSORS) is not None:
        hass.helpers.discovery.load_platform(
            PLATFORM, DOMAIN, conf[CONF_SENSORS], config
        )
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data={}
        )
    )
    return True


async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""
    hass.async_create_task(hass.config_entries.async_remove(config_entry.entry_id))
    return True


async def async_remove_entry(hass, config_entry):
    """Handle removal of an entry."""
    try:
        await hass.config_entries.async_forward_entry_unload(config_entry, PLATFORM)
        _LOGGER.info(
            "Successfully removed sensor from the garbage_collection integration"
        )
    except ValueError:
        pass


async def update_listener(hass, entry):
    """Update listener."""
    entry.data = entry.options
    await hass.config_entries.async_forward_entry_unload(entry, PLATFORM)
    hass.async_add_job(hass.config_entries.async_forward_entry_setup(entry, PLATFORM))


class ConnectionPlatform:
    def __init__(
        self,
        account_key,
    ):
        self.__account_key = account_key
        self.__api = LTADataMall(account_key)

    def get_arrival_times(self, bus_stop_number, service_number):
        return self.__api.get_arrival_times(
            bus_stop_number,
            service_number,
        )
    
    def get_train_disruptions(self):
        return self.__api.get_train_disruptions()

