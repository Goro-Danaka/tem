import json
import requests

from providers.logging_provider import LoggingProvider


class Browser:
    _user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
    _accept_language = 'ru,en-US;q=0.9,en;q=0.8,de;q=0.7'

    _proxy_service_url = 'https://api.getproxylist.com/proxy?apiKey=%s'

    _settings = None

    _proxy_api_key = None

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

    def get_html(self, url, use_proxy=False):
        try:
            if use_proxy and self._proxy_api_key:
                proxy_dict = self.get_proxy()
                response = self.session.get(url, proxies=proxy_dict)
            else:
                response = self.session.get(url)
            html_page = response.content
            return html_page
        except Exception as ex:
            self.logging_provider.critical('Error in method get_html: url - %s\nException: \n%s' % (url, ex))

    def get_proxy(self):
        proxy_dict = {}
        try:
            response = self.session.get(self._proxy_service_url % self._proxy_api_key)
            json_response = json.loads(response.text)
            ip = json_response['ip']
            port = json_response['port']
            protocol = json_response['protocol']
            proxy_dict = {
                protocol: '%s://%s:%s' % (protocol, ip, port)
            }
        except Exception as ex:
            self.logging_provider.warning('Can\'t get proxy. Exception: \n"%s"' % ex)
        finally:
            return proxy_dict

    def set_settings(self, settings):
        if not settings:
            return
        self._settings = settings
        self._proxy_api_key = self._settings.proxy_api



