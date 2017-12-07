import datetime

from lxml import html
from scripts.caravancampingsales.categories import Categories
from scripts.providers.logging_provider import LoggingProvider
from scripts.providers.databases.database_provider import DatabaseProvider
from scripts.providers.databases.db_type import DBType
from scripts.caravancampingsales.page_info import PageInfo

class ResultListInfo:


    base_url = 'https://www.caravancampingsales.com.au%s'
    query_url = 'https://www.caravancampingsales.com.au/buy/results/?q=%s'

    page_link_xpath = '//a[@class="item-link-container"]'
    next_result_page_xpath = '//div[@class="pagination auxiliary"]/ul/li/a'


    def __init__(self, browser_instance):
        self.browser = browser_instance
        self.logging_provider = LoggingProvider()
        self.page_info_instance = PageInfo(self.browser)
        self.database_provider_instance = DatabaseProvider('caravancampingsales')
        for category in Categories:
            self.get_page_result_content(category)
        self.database_provider_instance.export_to_csv()


    def get_category_url(self, category):
        if category in Categories:
            return self.query_url % Categories[category]

    def get_page_links(self, url):
        try:
            content = self.browser.get_html(url)
            content_tree = html.fromstring(content)
            page_links_list = list()
            page_links_href_list = content_tree.xpath(self.page_link_xpath)
            if len(page_links_href_list):
                for page_link_href in page_links_href_list:
                    page_link = self.base_url % (page_link_href.attrib['href'])
                    page_links_list.append(page_link)
                return page_links_list
            else:
                self.logging_provider.critical('page_links_href_list is empty.')
                return None
        except Exception as ex:
            self.logging_provider.critical('Error in get_page_links. Exception: \n%s' % ex)

    def get_next_result_page_url(self, url):
        try:
            content = self.browser.get_html(url)
            content_tree = html.fromstring(content)
            next_result_page_list = content_tree.xpath(self.next_result_page_xpath)
            if len(next_result_page_list):
                last_page_list = next_result_page_list[-1]
                if last_page_list.text and last_page_list.text == 'Next':
                    next_result_page_url = self.base_url % (next_result_page_list[-1].attrib['href'])
                    return next_result_page_url
                else:
                    self.logging_provider.info("Next result page url not found. For url: %s" % url)
                    return None
            else:
                self.logging_provider.info("Next result page url not found. For url: %s" % url)
                return None
        except Exception as ex:
            self.logging_provider.info("Next result page url not found. Exception: \n%s" % ex)

    def get_page_result_content(self, category):
        try:
            page_url = self.get_category_url(category)
            has_next_result_page = True
            i = 1
            while has_next_result_page:
                object_page_urls = self.get_page_links(page_url)
                next_page_url = self.get_next_result_page_url(page_url)
                has_next_result_page = True if next_page_url and len(next_page_url) > 0 else False
                self.logging_provider.info('[%s] Result page. Page number %s, url: %s' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i, page_url))
                count = 0
                if object_page_urls:
                    for object_page_url in object_page_urls:
                        object_info = self.page_info_instance.get_full_object_info(object_page_url)
                        if object_info and len(object_info.keys()) > 0:
                            self.database_provider_instance.insert(object_info)
                        else:
                            self.logging_provider.info('[%s] Object info empty. Page url: %s'
                                                       % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                          object_page_url))
                        count += 1
                        self.logging_provider.info('[%s] Scraped info. Page number %s, url: %s' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), count, object_page_url))
                else:
                    self.logging_provider.warning('[%s] page_urls is empty' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                page_url = next_page_url
                i += 1
        except Exception as ex:
            self.logging_provider.critical("Error in get_page_result_content. Exception: \n%s" % (ex))
