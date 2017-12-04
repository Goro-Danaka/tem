from lxml import html
from providers.logging_provider import LoggingProvider


class SProducts:

    product_links_xpath = '//a[@class="grid-product__image-link"]'
    next_page_xpath = '//span[@class="next"]/a'
    base_url = None

    def __init__(self, browser):
        self.browser = browser
        self.lp = LoggingProvider()

    def get_products(self, base_url, category_url):
        page_number = 0
        has_next_page = True
        self.base_url = base_url
        content = self.browser.get_html(category_url)
        content_tree = html.fromstring(content)
        while has_next_page:
            has_next_page = self.has_next_page(content_tree)
            product_urls = self.get_product_urls(content_tree)
            for product_url in product_urls:
                pass

    def has_next_page(self, content_tree):
        next_page = content_tree.xpath(self.next_page_xpath)
        if next_page and len(next_page):
            return True
        return False

    def get_product_urls(self, content_tree):
        product_urls = list()
        try:
            product_links = content_tree.xpath(self.product_links_xpath)
            if not product_links or not len(product_links):
                self.lp.info('Product links not found. ')
                return product_urls
            for product_link in product_links:
                if 'href' in product_link.attrib:
                    product_url = self.base_url + product_link.attrib['href']
                    product_urls.append(product_url)
                else:
                    self.lp.warning('Product link: %s hasn\'t href attribute' % product_link)
        except Exception as ex:
            self.lp.critical('Exception occurred while getting product urls. Exception: \n%s' % ex)
        finally:
            return product_urls





