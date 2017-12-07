import datetime

from lxml import html

from scripts.pitchup.locations import Locations
from scripts.pitchup.page_info import PageInfo
from scripts.providers.databases.database_provider import DatabaseProvider
from scripts.providers.logging_provider import LoggingProvider


class ResultListInfo:

    base_url = 'http://www.pitchup.com%s'
    park_list_url = 'http://www.pitchup.com/campsites/%s'
    park_list_url_with_page = 'http://www.pitchup.com/campsites/%s?page=%s'

    '''
    Page list info elements xpath's
    '''

    page_link_xpath = '//a[@class="campsite-name"]'
    page_selected_xpath = '//div[@class="paging"]/div[@style="text-align: center"]'
    next_result_page_xpath = '//a[@class="prevnext ajax"]'

    result_page_url = '?page=%s'

    parks_per_list_page = 20
    expected_list_pages = 0

    def __init__(self, browser_instance):
        self.browser = browser_instance
        self.logging_provider = LoggingProvider()
        self.park_page_info_instance = PageInfo(self.browser)
        self.database_provider_instance = DatabaseProvider('pitchup')
        for key in Locations:
            self.get_page_result_content(key)
        self.database_provider_instance.export_to_csv()

    def get_page_result_content(self, location):
        self.get_parks_full_info(location)

    def get_location_url(self, location):
        if location in Locations:
            return self.park_list_url % Locations[location]

    def get_location_url_with_page(self, location, page_number):
        if location in Locations:
            return self.park_list_url_with_page % (Locations[location], page_number)

    def get_park_page_links(self, url):
        try:
            content = self.browser.get_html(url)
            content_tree = html.fromstring(content)
            park_page_links_list = list()
            park_page_links_href_list = content_tree.xpath(self.page_link_xpath)
            if len(park_page_links_href_list):
                for park_page_link_href in park_page_links_href_list:
                    park_page_link = self.base_url % (park_page_link_href.attrib['href'])
                    park_page_links_list.append(park_page_link)
                return park_page_links_list
            else:
                self.logging_provider.critical('park_page_links_href_list is empty.')
                return None
        except Exception as ex:
            self.logging_provider.critical('Error in get_page_links. Exception: \n%s' % ex)


    def get_next_result_page_url(self, url):
        try:
            content = self.browser.get_html(url)
            content_tree = html.fromstring(content)
            next_result_page_list = content_tree.xpath(self.next_result_page_xpath)
            if len(next_result_page_list):
                next_result_page_url = self.base_url % (next_result_page_list[0].attrib['href'])
                return next_result_page_url
            else:
                return None
        except Exception as ex:
            self.logging_provider.info("Next result page url not found. Exception: \n%s" % (ex))

    def get_parks_full_info(self, location):
        try:
            parks_info = list()
            has_next_result_page = True
            i = 1
            while has_next_result_page:
                page_url = self.get_location_url_with_page(location, i)
                park_page_urls = self.get_park_page_links(page_url)
                next_page_url = self.get_next_result_page_url(page_url)
                has_next_result_page = True if next_page_url and len(next_page_url) > 0 else False
                self.logging_provider.info('[%s] Result page. Page number %s, url: %s' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i, page_url))
                count = 0
                if park_page_urls:
                    for park_page_url in park_page_urls:
                        full_park_info = self.park_page_info_instance.get_full_park_info(park_page_url)
                        self.database_provider_instance.insert(full_park_info)
                        count+=1
                        self.logging_provider.info('[%s] Scraped park info. Park number %s, url: %s' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), count, park_page_url))
                else:
                    self.logging_provider.warning('[%s] park_page_urls is empty' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                i+=1
            return parks_info
        except Exception as ex:
            self.logging_provider.critical("Error in get_parks_full_info. Exception: \n%s" % (ex))


