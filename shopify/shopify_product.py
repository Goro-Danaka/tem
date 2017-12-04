from providers.logging_provider import LoggingProvider
from lxml import html


class SProduct:

    in_stock_schema = 'http://schema.org/InStock'

    product_title_xpath = '//meta[@property="og:title"]'
    product_url_xpath = '//meta[@property="og:url"]'
    product_description_xpath = '//meta[@property="og:description"]'
    product_images_xpath = '//meta[@property="og:image"]'
    product_price_xpath = '//meta[@property="og:price:amount"]'
    product_currency_xpath = '//meta[@property="og:price:currency"]'

    product_sale_price_xpath = '//span[@class="product-single__price on-sale"]'
    product_availability = '//link[@itemprop="availability"]'

    def __init__(self, browser):
        self.browser = browser
        self.lp = LoggingProvider()

    def get_product_meta_info(self, product_url):
        content = self.browser.get_html(product_url)
        content_tree = html.fromstring(content)
        product_title_elements = content_tree.xpath(self.product_title_xpath)
        product_url_elements = content_tree.xpath(self.product_url_xpath)
        product_description_elements = content_tree.xpath(self.product_description_xpath)
        product_price_elements = content_tree.xpath(self.product_price_xpath)
        product_currency_elements = content_tree.xpath(self.product_currency_xpath)
        product_image_elements = content_tree.xpath(self.product_images_xpath)

        product_title = product_title_elements[0].attrib['content']\
            if len(product_title_elements) and \
               'content' in product_title_elements[0].attrib\
            else None

        product_url = product_url_elements[0].attrib['content'] \
            if len(product_url_elements) and \
               'content' in product_url_elements[0].attrib \
            else None

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

        product_images = SProduct.get_product_images(product_image_elements)

        product_meta_info = {
            'Title': product_title,
            'Url': product_url,
            'Description': product_description,
            'Price': product_price,
            'Currency': product_currency,
            'Images': product_images
        }

        return product_meta_info

    def is_product_available(self, content_tree):
        available_element = content_tree.xpath(self.product_availability)
        if available_element and len(available_element):
            if 'href' in available_element.attrib:
                schema_url = available_element.attrib['href']
                if schema_url == self.in_stock_schema:
                    return True
        return False

    @staticmethod
    def get_product_images(product_image_elements):
        image_urls = list()
        for product_image_element in product_image_elements:
            image_url = product_image_element.attrib['content'] \
                if 'content' in product_image_element.attrib \
                else None
            image_urls.append(image_url)
        return image_urls
