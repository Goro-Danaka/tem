from lxml import html

class PageInfo:

    good_title_xpath = '//div[@class="content-header"]/h1'
    item_details_xpath = '//section[@class="component item-details"]/section[@class and not(@class="description") and not(@class="Seller-Details")]'
    item_details_names_xpath = '//section[@class="component item-details"]/section[not(@class="description") and not(@class="Seller-Details")]/h2'
    item_details_selection_elements_names_xpath = '//section[@class="component item-details"]/section[@class="%s"]/table/tbody/tr/th'
    item_details_selection_elements_values_xpath = '//section[@class="component item-details"]/section[@class="%s"]/table/tbody/tr/td'

    personal_fields = ['Price', 'Reference Code', 'Last Modified Date', 'Rego Expiry', 'Registration', 'Warranty', 'State', 'Postcode',
                       'Phone', 'Need Finance?', 'Stock Number', 'Serial Number']

    def __init__(self, browser_instance):
        self.browser = browser_instance

    def get_full_object_info(self, url):
        content = self.browser.get_html(url)
        content_tree = html.fromstring(content)
        good_name = content_tree.xpath(self.good_title_xpath)
        item_datails_class_names_list = content_tree.xpath(self.item_details_xpath)
        item_details_names_list = content_tree.xpath(self.item_details_names_xpath)
        item_details = {}
        i = 0
        while i < len(item_details_names_list):
            item_name = item_details_names_list[i].text
            class_name = item_datails_class_names_list[i].attrib['class']
            item_details_selection_elements_names_list = content_tree.xpath(self.item_details_selection_elements_names_xpath % class_name)
            item_details_selection_elements_values_list = content_tree.xpath(self.item_details_selection_elements_values_xpath % class_name)
            j = 0
            while j < len(item_details_selection_elements_names_list):
                collumn_name = item_details_selection_elements_names_list[j].text
                if self.is_non_personal_info(item_details_selection_elements_names_list[j].text):
                    collumn_value = item_details_selection_elements_values_list[j].text
                    item_details[collumn_name] = collumn_value
                j+=1
            i+=1
        return item_details

    def is_non_personal_info(self, field_name):
        if field_name not in self.personal_fields:
            return True
