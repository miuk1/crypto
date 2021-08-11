import requests
from requests.api import head, request
import logging
logging.basicConfig(level=logging.ERROR)

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class MarketData:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def getMarketData(self):
        response_object = requests.get(self.base_url, self.headers)
        if response_object.status_code == 200:
            return response_object.json()
        else:
            log.error('Could not get response from api')
            log.error(response_object)
            return response_object.status_code
