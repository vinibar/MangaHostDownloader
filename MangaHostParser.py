# -*- coding: utf-8 -*-
import urllib.request ,urllib.error, urllib
import zipfile
import os
import re
from operator import itemgetter
from bs4 import BeautifulSoup as BS

class MangaHostParser():

    HDR = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

    SEARCH_URL = 'https://mangahost.net/find/'

    def _get_html(self, url):
        req = urllib.request.Request(url, headers=MangaHostParser.HDR)
        resource = urllib.request.urlopen(req)
        return resource.read()

    def search_for(self, title):
        title.replace('\s', '+')
        soup = BS(self._get_html(MangaHostParser.SEARCH_URL + title), "lxml")
        search_results = soup.find_all("h3", {"class": "entry-title"})

        manga_list = []
        for item in search_results:
            manga_list.append({'title': item.find('a').get('title'),
                               'url': item.find('a').get('href')})
        return manga_list

    def get_issues_list(self, url):
        soup = BS(self._get_html(url), "lxml")
        ul = soup.find("ul", {"class": "list_chapters"})
        a_list = ul.find_all('a')

        issues_list = []
        for a in a_list:
            s = BS(a.get('data-content'), "lxml")
            a2 = s.find('a')
            issues_list.append({"title": a.get('data-original-title'),
                                "url": a2.get('href'),
                                "id": int(a.get('id'))})
        return sorted(issues_list, key=itemgetter('id'))

    def get_pages_from_url(self, url):
        links = re.search("(var images \= \[)(.+)(\])", self._get_html(url).decode('utf-8')).group(2)
        links = links.replace('"', '').split(",")

        i = 0
        while i < len(links):
            links[i] = re.search(r"(?<=src=').*?(?=')", links[i]).group(0)
            i+=1
        return links

    def get_filename(self, url):
        splitted_url = url.split("/")
        return splitted_url[-1]

    def download_url(self, url):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', MangaHostParser.HDR['User-Agent'])]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, self.get_filename(url))

    def download_issue_none(self, url):
        for page in self.get_pages_from_url(url):
            self.download_url(page)

    def download_issue_zip(self, url):
        names = []
        zip = zipfile.ZipFile('teste.zip', 'a')
        for page in self.get_pages_from_url(url):
            self.download_url(page)
            names.append(self.get_filename(page))

        for name in names:
            zip.write(name)
            os.remove(name)
        zip.close()

    def download_issue(self, url, mode=None):
        if mode == None:
            self.download_issue_none(url)
        elif mode == 'zip':
            self.download_issue_zip(url)
        else:
            pass