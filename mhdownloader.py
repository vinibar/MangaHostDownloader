# -*- coding: utf-8 -*-
import os
import urllib.request ,urllib.error, urllib
from mhparser import MangaHostParser


class MangaHostDownloader:

    def download_url(self, url, path=""):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', MangaHostParser.HDR['User-Agent'])]
        urllib.request.install_opener(opener)
        file_path = path + self.get_filename(url)
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        urllib.request.urlretrieve(url, file_path)

    def get_filename(self, url):
        splitted_url = url.split("/")
        return splitted_url[-1]