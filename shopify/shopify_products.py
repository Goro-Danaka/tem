from lxml import html
from shopify.shopify_product import SProduct
from providers.logging_provider import LoggingProvider


class SProducts:

    _page_url_tail = '?page=%s'
    _product_links_xpath = '//a[re:test(@href, "(\\/)(collections)(\\/)((?:[a-z][a-z0-9_-]*))' \
                           '(\\/)(products)(\\/)((?:[a-z][a-z0-9_-]*))$")]'
    _next_page_xpath = '//a[contains(@href, "?page=")]'
    _base_url = None

    _in_progress = False

    def __init__(self, browser):
        self.browser = browser
        self.product_provider = SProduct(browser=browser)
        self.lp = LoggingProvider()

    def get_products(self, base_url, category):
        self._in_progress = True
        category_url = category['link']
        category_title = category['title']
        page_number = 1
        products_info_list = list({})
        has_next_page = True
        self._base_url = base_url
        while has_next_page:
            if not self._in_progress:
                return products_info_list
            full_category_url = category_url + self._page_url_tail % page_number
            content = self.browser.get_html(full_category_url)
            content_tree = html.fromstring(content)
            has_next_page = self._has_next_page(content_tree)
            product_urls = self._get_product_urls(content_tree)
            for product_url in product_urls:
                if not self._in_progress:
                    return products_info_list
                product_info = self.product_provider.get_product_info(product_url, category_title)
                products_info_list.append(product_info)
            page_number += 1
        self._in_progress = False
        return products_info_list

    def _has_next_page(self, content_tree):
        next_page = content_tree.xpath(self._next_page_xpath)
        if next_page and len(next_page):
            if not next_page[-1].text.isdigit():
                return True
            else:
                return False
        return False

    def _get_product_urls(self, content_tree):
        product_urls = list()
        try:
            product_links = content_tree.xpath(self._product_links_xpath,
                                               namespaces={'re': "http://exslt.org/regular-expressions"})
            if not product_links or not len(product_links):
                self.lp.info('Product links not found. ')
                return product_urls
            for product_link in product_links:
                if not self._in_progress:
                    return product_urls
                if 'href' in product_link.attrib:
                    product_url = self._base_url + product_link.attrib['href']
                    if product_url not in product_urls:
                        product_urls.append(product_url)
                else:
                    self.lp.warning('Product link: %s hasn\'t href attribute' % product_link)
        except Exception as ex:
            self.lp.critical('Exception occurred while getting product urls. Exception: \n%s' % ex)
        finally:
            return product_urls

    def stop(self):
        self._in_progress = False





