import requests
import re

from config import settings


def get_main_download_link(link):
    response = requests.get(link)
    page_content = response.text

    re_pattern = r'dispatcher.*?weblink_get.*?url":"(.*?)"'
    match = re.search(re_pattern, page_content)

    if match:
        url = match.group(1)
        parts = link.split('/')[-2:]
        url = f'{url}/{parts[0]}/{parts[1]}'
        return url

    return None


def download_file():
    data = requests.get(get_main_download_link(settings.DOWNLOAD_URL))
    with open(f"{settings.CURRENT_FILE_NAME}.{settings.CURRENT_FILE_EXTENSION}", 'wb') as file:
        file.write(data.content)

