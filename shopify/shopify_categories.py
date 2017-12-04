import re

from lxml import html
from config.config import defaults
from providers.logging_provider import LoggingProvider


class SCategories:

    categories_links_xpath = '//a[@class="collection-grid__item-link collection-collage__item-wrapper"]'
    categories_titles_xpath = '//span[@class="collection-grid__item-title"]'

    def __init__(self, browser):
        self.lp = LoggingProvider()
        self.browser = browser

    def get_categories(self, url):
        try:
            url = SCategories.get_categories_page(url)
            content = self.browser.get_html(url)
            content_tree = html.fromstring(content)
            categories_links = content_tree.xpath(self.categories_links_xpath)
            categories_titles = content_tree.xpath(self.categories_titles_xpath)
            categories = self.get_categories_info(categories_links, categories_titles)
        except Exception as ex:
            self.lp.critical('Can\'t get categories. Url: %s; Exception: \n%s' % (url, ex))
        finally:
            return categories

    def get_categories_info(self, categories_links, categories_titles):
        categories_info = list()
        i = 0
        try:
            categories_links_length = len(categories_links)
            categories_titles_length = len(categories_titles)
            if categories_links_length != categories_titles_length:
                self.lp.warning('Categories links and name has different sizes.')
            while i < categories_links_length:
                category_title = categories_titles[i].text
                category_link = categories_links[i].attrib['href']
                category_info = {
                    'title': category_title,
                    'link': category_link
                }
                categories_info.append(category_info)
        except Exception as ex:
            self.lp.critical('Can\'t get categories info.'
                             ' links: \n%s; titles: \n%s; Exception: \n%s'
                             % (categories_links, categories_titles, ex))
        finally:
            return categories_info

    @staticmethod
    def get_categories_page(url):
        if re.match(defaults['products_url_template'], url):
            return url
        return url + defaults['products_url']
