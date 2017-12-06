from shopify.shopify_categories import SCategories
from shopify.shopify_products import SProducts
from shopify.shopify_product import SProduct

from providers.logging_provider import LoggingProvider


class ShopifyScraper:
    def __init__(self, browser, url='https://9gifts.net'):
        self.lp = LoggingProvider()
        self.categories_provider = SCategories(browser=browser)
        self.products_provider = SProducts(browser=browser)
        self.product_provider = SProduct(browser=browser)
        self.scrape_categories(url)

    def scrape_categories(self, url):
        all_products_list = list()
        categories = self.categories_provider.get_categories(url=url)
        for category in categories:
            self.lp.info('Scraper category: %s' % category['title'])
            products = self.products_provider.get_products(url, category['link'])
            all_products_list.extend(products)
        return all_products_list
