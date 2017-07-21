# -*- coding: utf-8 -*-
import urllib.request ,urllib.error, urllib

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
        try:
            soup = BS(self._get_html(MangaHostParser.SEARCH_URL + title), "lxml")
        except urllib.error.URLError:
            print("Não foi possível conectar ao MangaHost.net.")
            exit(0)
        search_results = soup.find_all("h3", {"class": "entry-title"})

        manga_list = []
        for item in search_results:
            manga_list.append({'title': item.find('a').get('title'),
                               'url': item.find('a').get('href')})
        return manga_list

    def get_issues_list(self, url):
        soup = BS(self._get_html(url), "lxml")
        ul = soup.find("ul", {"class": "list_chapters"})
        issues_list = []
        special_issues_list = []
        spcount = 10000
        if ul:
            a_list = ul.find_all('a')
            for a in a_list:
                s = BS(a.get('data-content'), "lxml")
                a2 = s.find('a')

                id = 0
                if a.get('id').isdigit():
                    id = int(a.get('id'))
                else:
                    spcount -= 1
                    id = spcount
                    special_issues_list.append({"title": a.get('data-original-title'),
                                                "url": a2.get('href'),
                                                "id": spcount})

                issues_list.append({"title": a.get('data-original-title'),
                                    "url": a2.get('href'),
                                    "id": id})

        else:
            a_list = soup.find_all("a", {"class":"capitulo"})
            id = len(a_list)
            for a in a_list:
                issues_list.append({"title": a.contents[0],
                                    "url": a.get('href'),
                                    "id": id})
                id -= 1

        return sorted(issues_list, key=itemgetter('id')), sorted(special_issues_list, key=itemgetter('id'))

    def get_pages_from_url(self, url):
        links = re.search("(var images \= \[)(.+)(\])", self._get_html(url).decode('utf-8')).group(2)
        links = links.replace('"', '').split(",")

        i = 0
        while i < len(links):
            links[i] = re.search(r"(?<=src=').*?(?=')", links[i]).group(0)
            i+=1
        return links