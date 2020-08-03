"""
LTADataMall partial API
"""
import logging
import json
# from datetime import datetime, date, time, timedelta
import requests

HTTP_TIMEOUT = 10

_LOGGER = logging.getLogger(__name__)

BUS_ARRIVAL_URL = "http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2"
TRAIN_SERVICE_URL = "http://datamall2.mytransport.sg/ltaodataservice/TrainServiceAlerts"

class LTADataMall:

    """Constructor"""
    def __init__(self, account_key):
        """Setup of the LTADataMall library"""
        self._account_key = account_key
        self._headers = { 'AccountKey': self._account_key }

    def get_arrival_times(self, bus_stop_code, service_no):
        """List combination IDs available for the user account"""
        payload = {"BusStopCode": bus_stop_code, "ServiceNo": service_no}
        try:
            result = requests.get(
                BUS_ARRIVAL_URL,
                headers=self._headers,
                params=payload,
                timeout=HTTP_TIMEOUT).json()

        except Exception as e:
            _LOGGER.error(f"Exception reading response: {e.args}")
        return result

    def get_train_disruptions(self):
        """Train disruption"""
        try:
            result = requests.get(
                TRAIN_SERVICE_URL,
                headers=self._headers,
                timeout=HTTP_TIMEOUT).json()
            return result

        except Exception as e:
            _LOGGER.error(f"Exception reading response: {e.args}")
        return "Failed to get train disruption info"
