import re


from shopify.shopify_categories import SCategories
from shopify.shopify_products import SProducts
from shopify.shopify_product import SProduct

from urllib.parse import urlparse
from providers.logging_provider import LoggingProvider


class ShopifyScraper:

    _robots_url_tile = '/robots.txt'
    _is_shopify_regex = '(\\/)(\\d+)(\\/)(checkouts)'

    def __init__(self, browser, url='https://9gifts.net/lol/test'):
        domain_url = ShopifyScraper._get_url_domain(url)
        self.browser = browser
        self.lp = LoggingProvider()
        self.categories_provider = SCategories(browser=browser)
        self.products_provider = SProducts(browser=browser)
        self.product_provider = SProduct(browser=browser)
        self.scrape_categories(domain_url)

    def scrape_categories(self, url):
        all_products_list = list()
        is_shopify = self.is_shopify_site(url)
        if not is_shopify:
            self.lp.critical('Site: "%s" is not shopify based. Skipped.' % url)
            return all_products_list
        categories = self.categories_provider.get_categories(url=url)
        for category in categories:
            self.lp.info('Scraper category: %s' % category['title'])
            products = self.products_provider.get_products(url, category['link'])
            all_products_list.extend(products)
        return all_products_list

    def is_shopify_site(self, url):
        robots_url = url + self._robots_url_tile
        content = str(self.browser.get_html(robots_url))
        if len(re.findall(pattern=self._is_shopify_regex, string=content)):
            return True
        return False

    @staticmethod
    def _get_url_domain(url):
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        return domain

