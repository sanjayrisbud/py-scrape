# Class that should be subclassed by all robots using the "requests" library
import random

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from shadow_useragent import ShadowUserAgent

from .robot import Robot


class RawRequests(Robot):

    _session = None
    _retries = 3
    _timeout = 10
    _status_forcelist = (500, 502, 503, 504)
    _proxypool = [
        "119.28.222.222:2282",
        "113.160.234.147:56570",
        "115.127.109.2:45067",
        "178.128.85.255:3128",
        "202.162.211.46:30161",
    ]
    use_proxies = True
    use_random_agents = True

    def __init__(self, args):
        super(RawRequests, self).__init__(args)
        self._session = requests.Session()

    def send_request(self, method, url, **kwargs):
        retries = kwargs.get("retries", self._retries)
        kwargs.pop("retries", None)
        retry = Retry(
            total=retries, backoff_factor=1, status_forcelist=self._status_forcelist
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount("http://", adapter)
        self._session.mount("https://", adapter)

        timeout = kwargs.get("timeout", self._timeout)
        kwargs.update({"timeout": timeout})

        headers = kwargs.get("headers", {})
        if self.use_random_agents:
            headers.update({"User-Agent": ShadowUserAgent().random_nomobile})
        else:
            headers.update(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) " +
                                    "AppleWebKit/537.36 (KHTML, like Gecko) " +
                                    "Chrome/78.0.3904.97 Safari/537.36 OPR/65.0.3467.48"
                }
            )
        kwargs.update({"headers": headers})

        if self.use_proxies:
            proxy = random.choice(self._proxypool)
            kwargs["proxies"] = {"http": proxy, "https": proxy}
            self.logger.debug(f"Using proxy {proxy}")

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
