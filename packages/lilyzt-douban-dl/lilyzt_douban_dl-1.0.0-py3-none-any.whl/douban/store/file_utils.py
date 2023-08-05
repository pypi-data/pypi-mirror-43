import os
import time

import requests


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_album_raw():

    pass



def save_from_url(url, headers, name, index):
    r = requests.get(url, headers = headers, stream = True)
    with open(name, 'wb') as f:
        f.write(r.content)
    time.sleep(0.5)
