# -*- coding: utf-8 -*-
import urllib.request ,urllib.error, urllib
from MangaHostParser import MangaHostParser
class Downloader:

    def download_url(self, url, path=""):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', MangaHostParser.HDR['User-Agent'])]
        urllib.request.install_opener(opener)
        file_path = path + self.get_filename(url)
        urllib.request.urlretrieve(url, file_path)

    def get_filename(self, url):
        splitted_url = url.split("/")
        return splitted_url[-1]