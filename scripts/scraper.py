import os
import sys
import json

from scripts.pitchup.scraper_pitchup import PitchUpScraper
from scripts.caravancampingsales.scraper_caravancampingsales import CaravanCampingSalesScraper


class Scraper:

    in_progress = False
    pages_list_info_instance = None
    scraper_scripts = None
    selected_script_name = None

    def __init__(self, script_name='PitchUp', phantom_path=None):
        self.scraper_scripts = {
            'PitchUp': PitchUpScraper(phantom_path=phantom_path),
            'CaravanCampingSales': CaravanCampingSalesScraper()
        }
        self.selected_script_name = script_name

    def select_script(self, script_name):
        self.selected_script_name = script_name

    def selected_script(self):
        return self.scraper_scripts[self.selected_script_name]

    def get_selected_script_name(self):
        return self.selected_script_name

    def start(self):
        script = self.selected_script()
        script.start()

    def get_result_files(self):
        file_list = []
        result_path = os.path.normpath(os.path.join(sys.path[0], 'results'))
        if os.path.exists(result_path):
            for file in os.listdir(result_path):
                if file.endswith(".csv"):
                    file_list.append(file)
        return file_list

    def get_status(self):
        script = self.selected_script()
        status = script.get_status()
        status['result_files'] = self.get_result_files()
        json_status = json.dumps(status)
        return json_status

