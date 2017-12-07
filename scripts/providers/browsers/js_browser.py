from selenium import webdriver

from scripts.providers.logging_provider import LoggingProvider
from scripts.providers.proxy_provider import ProxyProvider
from scripts.config.config import defaults

class Browser:
    def __init__(self, phantom_path=None):
      self.logging_provider = LoggingProvider()
      self.is_proxy_enabled = defaults['pitchup']['proxy_enabled']
      self.proxy_provider = ProxyProvider()
      try:
        self.driver = webdriver.PhantomJS(service_args=self.proxy_provider.get_random_proxy(browser_type='selenium')) \
            if self.is_proxy_enabled else webdriver.PhantomJS()
      except Exception as ex:
          self.logging_provider.critical('Error while init PhantomJS; Exception: %s' % ex)

    def get_html(self, url):
      try:
          self.driver.get(url)
          html_page = self.driver.page_source
          return html_page
      except Exception as ex:
          self.logging_provider.critical('Error in method get_html: url - %s\nException: \n%s' % (url, ex))
