import json

from scripts.providers.logging_provider import LoggingProvider
from scripts.providers.browsers.js_browser import Browser
from scripts.pitchup.result_list_info import ResultListInfo


class PitchUpScraper:

    in_progress = False
    pages_list_info_instance = None

    def __init__(self, phantom_path=None):
        self.logging_provider = LoggingProvider()
        self.browser = Browser(phantom_path=phantom_path)

    def start(self):
        self.in_progress = True
        self.pages_list_info_instance = ResultListInfo(self.browser)
        self.in_progress = False

    def get_status(self):
        status = {
            'in_progress': self.in_progress,
            'messages': self.logging_provider.get_messages()
        }
        return status
