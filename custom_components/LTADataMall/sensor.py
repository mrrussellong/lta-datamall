"""Support for LTADataMall sensors."""
import voluptuous as vol
import logging
import homeassistant.util.dt as dt_util

from datetime import datetime, timedelta
from homeassistant.helpers import config_validation as cv
import time
from homeassistant.util import Throttle
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import (
    CONF_SCAN_INTERVAL,
    CONF_SENSORS,
    CONF_ENTITY_ID,
    CONF_NAME,
)
from .constants import (
    DOMAIN,
    PLATFORM,
    ICON_BUS,
    ICON_TRAIN,
    CONF_BUS_STOP_NUMBER,
    CONF_SERVICE_NUMBER,
    CONF_DESCRIPTION,
    CONF_WINDOW,
    CONF_START_TIME,
    CONF_END_TIME,
    ATTR_SERVICE_NUMBER,
    ATTR_BUS_STOP_NUMBER,
    ATTR_DURATION1,
    ATTR_DURATION2,
    ATTR_DURATION3,
    ATTR_NAME,
    SENSOR_SCHEMA,
)

_LOGGER = logging.getLogger(__name__)

HTTP_TIMEOUT = 5
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)
TRAIN_MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Setup sensor platform."""
    pass

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the sensor platform."""
    devs = []
    devs.append(LTADataMallTrainDisruptionSensor(hass))

    if discovery_info is not None:
        for sensor in discovery_info:
            devs.append(LTADataMallBusTimingSensor(hass, SENSOR_SCHEMA(sensor)))
    async_add_entities(devs, True)


class LTADataMallTrainDisruptionSensor(SensorEntity):
    def __init__(self, hass):
        self.__hass = hass
        self._state = "Unknown"
        self._description = None
        pass

    @property
    def state(self):
        return self._state
    
    @property
    def name(self):
        return "Train Disruptions"

    @property
    def icon(self):
        return ICON_TRAIN

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        res = {}
        res[CONF_DESCRIPTION] = self._description
        return res

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from NEA."""
        result = self.__hass.data[DOMAIN].get_train_disruptions()
        if result is None:
            return
        status = result["value"]["Status"]
        self._description = result["value"]
        _LOGGER.warn("train: %s", [status, result["value"]])

        if int(status) == 1:
            self._state = "No disruption"
        else:
            line = result["value"]["Line"]
            self._state = f"{line} DISRUPTION!!!"

class LTADataMallBusTimingSensor(SensorEntity):
    """Representation of a openroute service travel time sensor."""

    def __init__(self, hass, config):
        """Initialize the sensor."""

        self.__hass = hass
        self.__name = config.get(CONF_NAME)
        self.__bus_stop_number = config.get(CONF_BUS_STOP_NUMBER)
        self.__service_number = config.get(CONF_SERVICE_NUMBER)
        self.__window = config.get(CONF_WINDOW)
        self.__description = config.get(CONF_DESCRIPTION)
        self.__duration_1 = 0
        self.__duration_2 = 0
        self.__duration_3 = 0

    @property
    def name(self):
        """Return the name of the sensor."""
        return self.__name

    @property
    def bus_stop_number(self):
        """Return the bus stop number."""
        return self.__bus_stop_number

    @property
    def service_number(self):
        """Return the service number."""
        return self.__service_number

    @property
    def state(self):
        """Return the duration_1."""
        return self.__duration_1

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        res = {}
        res[ATTR_BUS_STOP_NUMBER] = self.bus_stop_number
        res[ATTR_SERVICE_NUMBER] = self.service_number
        res[ATTR_DURATION1] = self.__duration_1
        res[ATTR_DURATION2] = self.__duration_2
        res[ATTR_DURATION3] = self.__duration_3
        res[CONF_DESCRIPTION] = self.__description
        res[ATTR_NAME] = self.__name
        return res

    @property
    def icon(self):
        return ICON_BUS

    def should_update(self):
        if not self.__window:
            return True

        should_proceed = False

        for window in self.__window:
            start_time = window[CONF_START_TIME]
            end_time = window[CONF_END_TIME]

            current_start = datetime.now().replace(
                hour=start_time.hour, minute=start_time.minute, second=0, microsecond=0)
            current_end = datetime.now().replace(
                hour=end_time.hour, minute=end_time.minute, second=0, microsecond=0)
            now = datetime.now()
            
            if current_start < now and now < current_end:
                should_proceed = should_proceed or True
                break

        return should_proceed


    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from NEA."""
        if not self.should_update():
            not_updated = "Not updated"
            self.__duration_1 = not_updated
            self.__duration_2 = not_updated
            self.__duration_3 = not_updated
            return

        result = self.__hass.data[DOMAIN].get_arrival_times(self.bus_stop_number, self.service_number)
        if (result is None or
            result["Services"] is None or
            len(result["Services"]) == 0):
            return

        service = result["Services"][0]
        arrival1 = service["NextBus"]["EstimatedArrival"]
        arrival2 = service["NextBus2"]["EstimatedArrival"]
        arrival3 = service["NextBus3"]["EstimatedArrival"]

        now = time.mktime(dt_util.utcnow().timetuple())
        date_format = '%Y-%m-%dT%H:%M:%S%z'
        try:
            if len(arrival1) != 0:
                arrival1 = datetime.strptime(arrival1, date_format)
                a1 = int(time.mktime(arrival1.timetuple()) - now) % 3600
                if a1 > 3400:
                    self.__duration_1 = "Arriving"
                else:
                    self.__duration_1 = round(a1 / 60, 2)
            

            if len(arrival2) != 0:
                arrival2 = datetime.strptime(arrival2, date_format)
                a2 = int(time.mktime(arrival2.timetuple()) - now) % 3600
                self.__duration_2 = round(a2 / 60, 2)
            

            if len(arrival3) != 0:
                arrival3 = datetime.strptime(arrival3, date_format)
                a3 = int(time.mktime(arrival3.timetuple()) - now) % 3600
                self.__duration_3 = round(a3 / 60, 2)

        except Exception as e:
            _LOGGER.warn(f"Exception reading public transport connection data: {e.args} {service}")
        
