import re

from datetime import datetime
from urllib.parse import urlparse

from shopify.shopify_categories import SCategories
from shopify.shopify_products import SProducts
from shopify.shopify_product import SProduct

from providers.logging_provider import LoggingProvider
from providers.request_browser import Browser


class ShopifyScraper:

    _robots_url_tile = '/robots.txt'
    _is_shopify_regex = '(\\/)(\\d+)(\\/)(checkouts)'

    _categories_provider = None
    _products_provider = None
    _product_provider = None
    _browser = None
    _lp = None

    _in_progress = False
    _is_job_finished = True
    _is_success = True
    _url = None
    _last_update_date = None
    _total_products = 0

    def __init__(self):
        self._browser = Browser()
        self._lp = LoggingProvider()

    def start(self, url):
        try:
            self.set_init_states()
            self._in_progress = True
            self._is_job_finished = False
            self._is_success = False
            self._url = url
            domain_url = ShopifyScraper._get_url_domain(url)
            self._categories_provider = SCategories(browser=self._browser)
            self._products_provider = SProducts(browser=self._browser)
            self._product_provider = SProduct(browser=self._browser)
            all_products_list = self.scrape_categories(domain_url)
            self._in_progress = False
            self._is_job_finished = True
            self._is_success = True
        except Exception as ex:
            self._lp.warning('Exception was thrown while scraping URL: "%s", Exception: \n"%s"' % (url, ex))
            self._is_job_finished = True
            self._in_progress = False
            self._is_success = False
        finally:
            self._last_update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._total_products = len(all_products_list)

    def set_init_states(self):
        self._in_progress = False
        self._is_job_finished = True
        self._is_success = True
        self._url = None
        self._last_update_date = None
        self._total_products = 0

    def scrape_categories(self, url):
        all_products_list = list()
        is_shopify = self.is_shopify_site(url)
        if not is_shopify:
            self._lp.critical('Site: "%s" is not shopify based. Skipped.' % url)
            return all_products_list
        categories = self._categories_provider.get_categories(url=url)
        for category in categories:
            if not self._in_progress:
                return all_products_list
            self._lp.info('Scraper category: %s' % category['title'])
            products = self._products_provider.get_products(url, category)
            all_products_list.extend(products)
        return all_products_list

    def is_shopify_site(self, url):
        robots_url = url + self._robots_url_tile
        content = str(self._browser.get_html(robots_url))
        if len(re.findall(pattern=self._is_shopify_regex, string=content)):
            return True
        return False

    def stop(self):
        self._in_progress = False
        if self._categories_provider:
            self._categories_provider.stop()
        if self._products_provider:
            self._products_provider.stop()

    def get_status(self):
        status = {
            'is_job_finished': self._is_job_finished,
            'url': self._url,
            'success': self._is_success,
            'last_update_date': self._last_update_date,
            'total_products': self._total_products
        }
        return status

    @staticmethod
    def _get_url_domain(url):
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return domain

