import requests
import os
import sys

from providers.logging_provider import LoggingProvider
from config.config import defaults


class Browser:
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
    accept_language = 'ru,en-US;q=0.9,en;q=0.8,de;q=0.7'

    def __init__(self):
        self.logging_provider = LoggingProvider()
        try:
            self.session = requests.Session()
            self.session.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': self.accept_language,
                'Cash-Control': 'max-age=0',
                'User-Agent': self.user_agent,
            })
        except Exception as ex:
            self.logging_provider.critical('Error while init request session; Exception: %s' % ex)

    def get_html(self, url):
        try:
            response = self.session.get(url)
            html_page = response.content
            return html_page
        except Exception as ex:
            self.logging_provider.critical('Error in method get_html: url - %s\nException: \n%s' % (url, ex))

    def download_file(self, image_url, config, filename):
        try:
            local_filename = filename
            r = self.session.get(image_url, stream=True)
            result_path = os.path.join(sys.path[0], 'result')
            result_path = os.path.join(result_path, defaults[config]['result_dir_template'])
            if not os.path.exists(result_path):
                os.makedirs(result_path)
            file_path = os.path.join(result_path, local_filename.lower())
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            return local_filename
        except:
            pass
