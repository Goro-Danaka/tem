import json

from scripts.providers.logging_provider import LoggingProvider
from scripts.providers.browsers.request_browser import Browser
from scripts.caravancampingsales.result_list_info import ResultListInfo


class CaravanCampingSalesScraper:
    in_progress = False
    result_list_info = None

    def __init__(self):
        self.logging_provider = LoggingProvider()
        self.browser = Browser()

    def start(self):
        self.in_progress = True
        self.result_list_info = ResultListInfo(self.browser)
        self.in_progress = False

    def get_status(self):
        status = {
            'in_progress': self.in_progress,
            'messages': self.logging_provider.get_messages()
        }
        return status

if __name__ == '__main__':
    app = CaravanCampingSalesScraper()
    app.start()
