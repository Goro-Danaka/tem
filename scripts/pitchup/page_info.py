from lxml import html


class PageInfo:

    '''
    Park info elements xpath's
    '''

    #park_title_xpath = '//meta[@property="og:title"]'
    park_title_xpath = '//div[@class="campsite-header clearfix"]/h1'
    park_latitude_xpath = '//meta[@property="place:location:latitude"]'
    park_longitude_xpath = '//meta[@property="place:location:longitude"]'

    park_grade_xpath = '//div[@class="side_box site_grade"]/span'
    park_features_xpath = '//div[@id="amenities"]/div/p[@class="active"]'
    park_all_features_xpath = '//div[@id="amenities"]/div/p'


    '''
    Park business contact elements xpath's
    '''
    park_street_address_xpath = '//meta[@property="business:contact_data:street_addres"]'
    park_locality_xpath = '//meta[@property="business:contact_data:locality"]'
    park_region_xpath = '//meta[@property="business:contact_data:region"]'
    park_country_name_xpath = '//meta[@property="business:contact_data:country_name"]'
    park_postal_code_xpath = '//meta[@property="business:contact_data:postal_code"]'


    url = "https://www.pitchup.com/campsites/England/South_West/Cornwall/Newquay/hendra-holiday-park/"

    def __init__(self, browser_instance):
        self.browser = browser_instance

    def get_full_park_info(self, url):
        content = self.browser.get_html(url)
        content_tree = html.fromstring(content)
        park_info = self.get_park_info(content_tree)
        park_business_contact_info = self.get_park_business_contact_info(content_tree)
        full_park_info = self.merge_two_dicts(park_info, park_business_contact_info)
        return full_park_info


    def get_park_info(self, content_tree):
        park_name_list = content_tree.xpath(self.park_title_xpath)
        park_latitude_list = content_tree.xpath(self.park_latitude_xpath)
        park_longitude_list = content_tree.xpath(self.park_longitude_xpath)
        park_grade_list = content_tree.xpath(self.park_grade_xpath)
        park_all_features_list = content_tree.xpath(self.park_all_features_xpath)

        park_name = park_name_list[0].text if len(park_name_list) else None
        park_latitude = park_latitude_list[0].attrib['content'] if len(park_latitude_list) else None
        park_longitude = park_longitude_list[0].attrib['content'] if len(park_longitude_list) else None
        park_grade = park_grade_list[0].attrib['title'][22:] if len(park_grade_list) else None
        park_features = self.get_park_all_features(park_all_features_list)

        park_info = {
            'name': park_name,
            'latitude': park_latitude,
            'longitude': park_longitude,
            'grade': park_grade,
        }

        all_park_info = self.merge_two_dicts(park_info, park_features)

        return all_park_info

    def get_park_business_contact_info(self, content_tree):
        park_street_address_list = content_tree.xpath(self.park_street_address_xpath)
        park_locality_list = content_tree.xpath(self.park_locality_xpath)
        park_region_list = content_tree.xpath(self.park_region_xpath)
        park_country_name_list = content_tree.xpath(self.park_country_name_xpath)
        park_postal_code_list = content_tree.xpath(self.park_postal_code_xpath)

        park_street_address = park_street_address_list[0].attrib['content'] if len(park_street_address_list) else None
        park_locality = park_locality_list[0].attrib['content'] if len(park_locality_list) else None
        park_region = park_region_list[0].attrib['content'] if len(park_region_list) else None
        park_country_name = park_country_name_list[0].attrib['content'] if len(park_country_name_list) else None
        park_postal_code = park_postal_code_list[0].attrib['content'] if len(park_postal_code_list) else None

        bussiness_contact_data = {
            'street_address': park_street_address,
            'locality': park_locality,
            'region': park_region,
            'country_name': park_country_name,
            'postal_code': park_postal_code,
        }

        return bussiness_contact_data

    def get_park_all_features(self, park_all_features_list):
        if not park_all_features_list or len(park_all_features_list) == 0:
            return None
        features = {}
        for feature_element in park_all_features_list:
            feature_name = feature_element.text
            features[feature_name] = 'True' if feature_element.attrib['class'] == 'active' else 'False'

        return features

    def get_park_active_features(self, park_features_list):
        if not park_features_list or len(park_features_list) == 0:
            return None
        features = list()
        for feature_element in park_features_list:
            features.append(feature_element.text)

        return features

    def merge_two_dicts(self, x, y):
        z = x.copy()
        z.update(y)
        return z