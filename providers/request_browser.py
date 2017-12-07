import time
import random
import requests

from providers.logging_provider import LoggingProvider


class Browser:
    _min_interval = 1
    _max_interval = 2
    _user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
    _accept_language = 'ru,en-US;q=0.9,en;q=0.8,de;q=0.7'

    def __init__(self):
        self.logging_provider = LoggingProvider()
        try:
            self.session = requests.Session()
            self.session.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': self._accept_language,
                'Cash-Control': 'max-age=0',
                'User-Agent': self._user_agent,
            })
        except Exception as ex:
            self.logging_provider.critical('Error while init request session; Exception: %s' % ex)

    def get_html(self, url):
        try:
            sleep_interval = random.randint(self._min_interval, self._max_interval)
            time.sleep(sleep_interval)
            response = self.session.get(url)
            html_page = response.content
            return html_page
        except Exception as ex:
            self.logging_provider.critical('Error in method get_html: url - %s\nException: \n%s' % (url, ex))

