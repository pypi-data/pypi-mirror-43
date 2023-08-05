
import argparse
import os
import re

from .album import get_album_by_id
from .vars import  STORE_PATH

def get_args():
    parser = argparse.ArgumentParser(prog = 'Douban Downloader', description = 'download douban images')
    parser.add_argument('url', help = 'please provide photo uri')
    parser.add_argument('path', default = STORE_PATH, nargs = '?', help = 'the path to store photo')
    return parser.parse_args()


def parse_args(url):
    match = re.match(r'https?://www.douban.com/photos/album/(\d+)', url)
    if match:
        album_id = match.group(1)
        get_album_by_id(album_id)
        return



    pass

def main():
    print("main from douban/command.py")
    args = get_args()
    STORE_PATH = args.path
    if args.url is not None:
        parse_args(args.url)

if __name__ == '__main__':
    main()

