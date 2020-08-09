"""
Text constants for LTADataMall sensor
"""
import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from datetime import datetime, date, time, timedelta

from homeassistant.const import (
    CONF_SCAN_INTERVAL,
    CONF_SENSORS,
    CONF_ENTITY_ID,
    CONF_NAME,
)

DOMAIN = "LTADataMall"
PLATFORM = "sensor"
VERSION = "0.0.1"
ISSUE_URL = "https://github.com/bruxy70/CZ-Public-Transport/issues"
ATTRIBUTION = "Data from this is provided by LTADataMall."


ICON_BUS = "mdi:bus"
ICON_TRAIN = "mdi:train"

CONF_ACCOUNT_KEY = "accountKey"
CONF_START_TIME = "startTime"
CONF_END_TIME = "endTime"

CONF_BUS_STOP_NUMBER = "busStopNumber"
CONF_SERVICE_NUMBER = "serviceNumber"
CONF_WINDOW = "window"
CONF_DESCRIPTION = "description"

ATTR_SERVICE_NUMBER = "Service Number"
ATTR_BUS_STOP_NUMBER = "Bus Stop Number"
ATTR_DURATION1 = "Duration1"
ATTR_DURATION2 = "Duration2"
ATTR_DURATION3 = "Duration3"
ATTR_NAME = "name"

DEFAULT_NAME = "LTADataMall"

WINDOW_SCHEMA = vol.Schema({
    vol.Optional(CONF_START_TIME, default="00:00"): cv.time,
    vol.Optional(CONF_END_TIME, default="23:59"): cv.time,
})

SENSOR_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_BUS_STOP_NUMBER): cv.string,
    vol.Required(CONF_SERVICE_NUMBER): cv.string,
    vol.Optional(CONF_DESCRIPTION): cv.string,
    vol.Optional(CONF_WINDOW): vol.All(cv.ensure_list, [WINDOW_SCHEMA]),
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_ACCOUNT_KEY, default=""): cv.string,
        vol.Optional(CONF_START_TIME, default="00:00"): cv.time,
        vol.Optional(CONF_END_TIME, default="23:59"): cv.time,
        vol.Optional(CONF_SENSORS): vol.All(cv.ensure_list, [SENSOR_SCHEMA]),
    }) },
    extra=vol.ALLOW_EXTRA,
)
