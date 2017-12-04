from providers.logging_provider import LoggingProvider
from lxml import html


class ProductFields:

    product_title_xpath = '//h1[@itemprop="name"]'
    product_price_xpath = '//span[@itemprop="price"]'
    product_currency_xpath = '//meta[@itemprop="priceCurrency"]'
    product_availability = '//link[@itemprop="availability"]'

    def __init__(self, browser):
        self.browser = browser

    def get_product_fields(self, product_url):
        content = self.browser.get_html(product_url)
        content_tree = html.fromstring(content)
        print(content)