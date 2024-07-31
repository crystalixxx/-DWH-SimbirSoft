import re
import requests


class UrlHandler:
    def __init__(self, row_url: str, resource: str):
        self.__row_url = row_url
        self.__resource = resource

    def handle_mail_cloud(self):
        response = requests.get(self.__row_url)
        page_content = response.text

        re_pattern = r'dispatcher.*?weblink_get.*?url":"(.*?)"'
        match = re.search(re_pattern, page_content)

        if match:
            url = match.group(1)
            parts = self.__row_url.split('/')[-2:]
            url = f'{url}/{parts[0]}/{parts[1]}'
            return url

        return None

    def hande_url(self):
        if self.__resource == 'mail':
            return self.handle_mail_cloud()
        else:
            raise ValueError(f'Ресурс {self.__resource} не поддерживается.')
