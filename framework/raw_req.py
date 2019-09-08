# Class that should be subclassed by all robots using the "requests" library
import random

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from .robot import Robot


class RawRequests(Robot):

    _session = None
    _retries = 3
    _timeout = 10
    _status_forcelist = (500, 502, 503, 504)
    _user_agents = ["a", "b", "c"]

    def __init__(self, args):
        super(RawRequests, self).__init__(args)
        self._session = requests.Session()

    def send_request(self, method, url, **kwargs):
        retries = kwargs.get("retries", self._retries)
        kwargs.pop("retries", None)
        retry = Retry(total=retries, backoff_factor=1, status_forcelist=self._status_forcelist)
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)

        timeout = kwargs.get("timeout", self._timeout)
        kwargs.update({"timeout": timeout})

        headers = kwargs.get("headers", {})
        headers.update({"User-Agent": random.choice(self._user_agents)})
        kwargs.update({"headers": headers})
        r = self._session.request(method, url, **kwargs)
        self.logger.debug(r.request.headers)
        return r

    def get(self, url, **kwargs):
        return self.send_request("GET", url, **kwargs)

    def post(self, url, **kwargs):
        return self.send_request("POST", url, **kwargs)

    def finalize(self):
        self._session.close()

    def run(self):
        raise NotImplementedError
