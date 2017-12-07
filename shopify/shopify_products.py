from lxml import html
from shopify.shopify_product import SProduct
from providers.logging_provider import LoggingProvider


class SProducts:

    _page_url_tail = '?page=%s'
    _product_links_xpath = '//a[@class="grid-product__image-link"]'
    _next_page_xpath = '//span[@class="next"]/a'
    _base_url = None

    def __init__(self, browser):
        self.browser = browser
        self.product_provider = SProduct(browser=browser)
        self.lp = LoggingProvider()

    def get_products(self, base_url, category_url):
        page_number = 1
        products_info_list = list({})
        has_next_page = True
        self._base_url = base_url
        while has_next_page:
            full_category_url = base_url + category_url + self._page_url_tail % page_number
            content = self.browser.get_html(full_category_url)
            content_tree = html.fromstring(content)
            has_next_page = self._has_next_page(content_tree)
            product_urls = self._get_product_urls(content_tree)
            for product_url in product_urls:
                product_info = self.product_provider.get_product_info(product_url)
                products_info_list.append(product_info)
            page_number += 1
        return products_info_list

    def _has_next_page(self, content_tree):
        next_page = content_tree.xpath(self._next_page_xpath)
        if next_page and len(next_page):
            return True
        return False

    def _get_product_urls(self, content_tree):
        product_urls = list()
        try:
            product_links = content_tree.xpath(self._product_links_xpath)
            if not product_links or not len(product_links):
                self.lp.info('Product links not found. ')
                return product_urls
            for product_link in product_links:
                if 'href' in product_link.attrib:
                    product_url = self._base_url + product_link.attrib['href']
                    product_urls.append(product_url)
                else:
                    self.lp.warning('Product link: %s hasn\'t href attribute' % product_link)
        except Exception as ex:
            self.lp.critical('Exception occurred while getting product urls. Exception: \n%s' % ex)
        finally:
            return product_urls





