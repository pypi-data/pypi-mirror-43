import os

import requests
from bs4 import BeautifulSoup

from .vars import headers
from .store import file_utils
from .store.file_utils import get_album_raw, save_from_url
from .thread_utils import threadPoolExecutor
from .vars import STORE_PATH

class Album(object):
    BASE_URL = 'https://www.douban.com/photos/album/'

    def __init__(self, album_id):
        self.url = self.BASE_URL + album_id
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')

    def photos(self):
        for photo_dom in self.__photos():
            photo_src = photo_dom.img['src']
            yield photo_src

    def __photos(self):
        return self.soup.find_all('div', class_ = 'photo_wrap')

def get_album(album):
    idx = 0
    file_utils.mkdir(STORE_PATH)
    for photo_url in album.photos():
        name = os.path.basename(photo_url)
        full_path = STORE_PATH + '/' + name
        if os.path.exists(full_path):
            continue
        threadPoolExecutor.submit(save_from_url, url = photo_url, headers = headers, name = full_path, index = idx)
        idx += 1





def get_album_by_id(album_id):
    album = Album(album_id)
    get_album(album)


