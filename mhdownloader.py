# -*- coding: utf-8 -*-
import os
import urllib.request ,urllib.error, urllib.parse, contextlib
from mhparser import *
from PIL import Image
import re

class MangaHostDownloader:

    def __init__(self):
        self._pattern = re.compile(".+\.jpg$")

    def download_url(self, url, path=""):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', MangaHostParser.HDR['User-Agent'])]
        urllib.request.install_opener(opener)
        file_path = path + self.get_filename(url)
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        urllib.request.urlretrieve(url, file_path)

        if not self._pattern.match(file_path):
            self.convert_to_jpg(file_path)

    def convert_to_jpg(self, file_path):

        parser = MangaHostParser()

        new_path_file = os.path.splitext(file_path)[0]
        if not self._pattern.match(new_path_file):
            new_path_file = new_path_file + '.jpg'

        im = Image.open(file_path).convert('RGB')
        try:
            im = parser.remove_borders(im)
        except(InvalidImage):
            os.remove(file_path)
            return None

        im.save(file_path, "jpeg")
        try:
            os.rename(file_path, new_path_file)
        except FileExistsError:
            os.remove(file_path)

    def get_filename(self, url):
        splitted_url = url.split("/")
        return splitted_url[-1]

    def convert_images_to_jpg(self):
        pass