from providers.logging_provider import LoggingProvider
from lxml import html


class SProduct:

    _in_stock_schema = 'http://schema.org/InStock'

    _product_title_xpath = '//meta[@property="og:title"]'
    _product_url_xpath = '//meta[@property="og:url"]'
    _product_description_xpath = '//meta[@property="og:description"]'
    _product_images_xpath = '//meta[@property="og:image"]'
    _product_price_xpath = '//meta[@property="og:price:amount"]'
    _product_currency_xpath = '//meta[@property="og:price:currency"]'

    _product_sale_price_xpath = '//span[@class="product-single__price on-sale"]'
    _product_availability = '//link[@itemprop="availability"]'

    def __init__(self, browser):
        self.browser = browser
        self.lp = LoggingProvider()

    def get_product_info(self, product_url, category_title):
        content = self.browser.get_html(product_url)
        content_tree = html.fromstring(content)
        product_meta_info = self._get_product_meta_info(content_tree, category_title, product_url)
        return product_meta_info

    def _get_product_meta_info(self, content_tree, category_title, product_url):
        product_title_elements = content_tree.xpath(self._product_title_xpath)
        #product_url_elements = content_tree.xpath(self._product_url_xpath)
        product_description_elements = content_tree.xpath(self._product_description_xpath)
        product_price_elements = content_tree.xpath(self._product_price_xpath)
        product_currency_elements = content_tree.xpath(self._product_currency_xpath)
        product_image_elements = content_tree.xpath(self._product_images_xpath)

        product_sale_price_elements = content_tree.xpath(self._product_sale_price_xpath)

        product_title = product_title_elements[0].attrib['content']\
            if len(product_title_elements) and \
               'content' in product_title_elements[0].attrib\
            else None

        #product_url = product_url_elements[0].attrib['content'] \
        #    if len(product_url_elements) and \
        #       'content' in product_url_elements[0].attrib \
        #    else None

        product_description = product_description_elements[0].attrib['content'] \
            if len(product_description_elements) and \
               'content' in product_description_elements[0].attrib \
            else None

        product_price = product_price_elements[0].attrib['content'] \
            if len(product_price_elements) and \
               'content' in product_price_elements[0].attrib \
            else None

        product_currency = product_currency_elements[0].attrib['content'] \
            if len(product_currency_elements) and\
               'content' in product_currency_elements[0].attrib \
            else None

        product_images = self._get_product_images(product_image_elements)

        is_product_available = self._is_product_available(content_tree)

        product_sale_price = product_sale_price_elements[0].attrib['content'] \
            if len(product_sale_price_elements) and \
               'content' in product_sale_price_elements[0].attrib \
            else None

        product_meta_info = {
            'Title': product_title,
            'Category': category_title,
            'Url': product_url,
            'Description': product_description,
            'Price': product_price,
            'Sale price': product_sale_price,
            'Currency': product_currency,
            'Images': product_images
        }

        self.lp.info('Scraped product: %s' % product_url)
        return product_meta_info

    def _is_product_available(self, content_tree):
        try:
            available_element = content_tree.xpath(self._product_availability)
            if available_element and len(available_element):
                if 'href' in available_element[0].attrib:
                    schema_url = available_element[0].attrib['href']
                    if schema_url == self._in_stock_schema:
                        return True
        except Exception as ex:
            self.lp.warning('Can\'t get product availability Exception: \n%s' % ex)
        finally:
            return False

    def _get_product_images(self, product_image_elements):
        try:
            image_urls = list()
            for product_image_element in product_image_elements:
                image_url = product_image_element.attrib['content'] \
                    if 'content' in product_image_element.attrib \
                    else None
                image_urls.append(image_url)
        except Exception as ex:
            self.lp.warning('Can\'t get product images. Exception: \n%s' % ex)
        finally:
            return image_urls
