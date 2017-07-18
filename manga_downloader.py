# -*- coding: utf-8 -*-
""" Manga Downloader
Download any manga from MangaHost (www.mangahost.net)


Attributes:
    hdr (list): HTTP Headers to access the links since there are some
        restriction rules imposed by the host's firewall

    base_url (string): Just a sample URL used for test purpose

Todo:
    * List all the mangas avaliable in the MangaHost.net
    * DOwnload complete collections or specific issues in ZIP
"""


import urllib.request ,urllib.error, urllib
import zipfile
import os
from bs4 import BeautifulSoup as BS
import re

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

base_url = "https://mangahost.net/manga/monster-mh40618/1"



def get_issues_from_url(url):
    """Self-explanatory name

    Args:
        url (str): The base URL for the manga
    Returns:
        list: links to the first page of all issues

    """
    req = urllib.request.Request(base_url, headers=hdr)
    resource = urllib.request.urlopen(req)
    soup = BS(resource.read(), "lxml")

    splitted_url = url.split("/")
    issues = []

    for item in soup.find_all('option'):
        try:

            splitted_url[-1] = item['id']
            issues.append("/".join(splitted_url))
        except KeyError as e:
            pass

    return sorted(issues)


def get_pages_from_url(url):
    """ Get all the pages from a single issue URL

    Args:
        url (str): the URL of the issue

    Returns:
        list: links to all pages

    """
    req = urllib.request.Request(base_url, headers=hdr)
    resource = urllib.request.urlopen(req)
    links = re.search("(var images \= \[)(.+)(\])", resource.read().decode('utf-8')).group(2)
    links = links.replace('"', '').split(",")

    i = 0
    while i < len(links):
        links[i] = re.search(r'(?<=src=\').*?(?=\')', links[i]).group(0)
        i+=1
    return links

def get_filename(url):
    splitted_url = url.split("/")
    return splitted_url[-1]

def download_url(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', hdr['User-Agent'])]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(url, get_filename(url))

def download_issue_none(url):
    for page in get_pages_from_url(url):
        download_url(page)

def download_issue_zip(url):
    names = []
    zip = zipfile.ZipFile('teste.zip', 'a')
    for page in get_pages_from_url(base_url):
        download_url(page)
        names.append(get_filename(page))

    for name in names:
        zip.write(name)
        os.remove(name)
    zip.close()

def download_issue(url, mode=None):
    if mode == None:
        download_issue_none(url)
    elif mode == 'zip':
        download_issue_zip(url)
    else:
        pass


#print(get_issues_from_url(base_url))
