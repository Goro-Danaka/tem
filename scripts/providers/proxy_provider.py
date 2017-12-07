import re
import random
import requests

from scripts.providers.logging_provider import LoggingProvider


class ProxyProvider:

    get_proxy_url = 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt'
    check_url = 'http://google.com'
    proxy_list = list({})
    ip_port_re = r'[0-9]+(?:\.[0-9]+){3}:[0-9]+'

    def __init__(self):
        self.logging_provider = LoggingProvider()
        self.session = requests.Session()
        self.is_proxy_list_updated = False

    def _check_proxy(self, requests_proxy):
        try:
            response = requests.get(self.check_url, proxies=requests_proxy)
            if response.status_code == 200:
                return True
            return False
        except Exception:
            return False

    def _get_proxies(self):
        try:
            response = self.session.get(self.get_proxy_url)
            if response.status_code != 200 or not response.content:
                self.logging_provider.warning('Get random proxy error. Status code: %s; Response content: \n%s' % (response.status_code, response.content))
                return self.proxy_list
            else:
                proxy_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', str(response.content))
                if not self.is_proxy_list_updated and len(self.proxy_list):
                    self.proxy_list = proxy_list
                return proxy_list
        except Exception as ex:
            self.logging_provider.warning('Get random proxy error. Exception: \n%s' % ex)
            return None

    def get_random_proxy(self, browser_type='requests'):
        proxy_list = self._get_proxies()
        ip_port = self._get_proxies()[random.randint(0, len(proxy_list))]
        requests_proxy_info = {
            'http': 'http://%s' % ip_port
        }

        is_good_proxy = self._check_proxy(requests_proxy_info)

        if not is_good_proxy:
            return self.get_random_proxy()

        selenium_proxy_info = ['--proxy=%s' % ip_port,
                               '--proxy-type=http']

        result = {
            'requests': requests_proxy_info,
            'selenium': selenium_proxy_info
        }

        if browser_type in result:
            return result[browser_type]

        return requests_proxy_info
