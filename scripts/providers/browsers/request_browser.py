import requests

from scripts.providers.logging_provider import LoggingProvider
from scripts.providers.proxy_provider import ProxyProvider
from scripts.config.config import defaults


class Browser:
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
    accept_language = 'ru,en-US;q=0.9,en;q=0.8,de;q=0.7'

    def __init__(self):
        self.is_proxy_enabled = defaults['caravancampingsales']['proxy_enabled']
        self.logging_provider = LoggingProvider()
        self.proxy_provider = ProxyProvider()
        try:
            self.session = requests.Session()
            self.session.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': self.accept_language,
                'Cash-Control': 'max-age=0',
                'User-Agent': self.user_agent,
            })
        except Exception as ex:
            self.logging_provider.critical('Error while init request session; Exception: %s' % ex)

    def get_html(self, url):
        try:
            response = self.session.get(url, proxies=self.proxy_provider.get_random_proxy()) if self.is_proxy_enabled \
                else self.session.get(url)
            html_page = response.content
            return html_page
        except Exception as ex:
            self.logging_provider.critical('Error in method get_html: url - %s\nException: \n%s' % (url, ex))
