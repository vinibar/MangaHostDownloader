# -*- coding: utf-8 -*-
import os
from Downloader import Downloader
from MangaHostParser import MangaHostParser

def choose_manga():
    choice = None
    while not choice:
        choice = input("Type the name of a manga you want: ")
    return choice

if __name__ == '__main__':
    print(' ---------------- MangaHost Downloader ----------------')
    print('* This program was created just for learning purposese.')
    print(' ------------------------------------------------------')
    print('\n\n')

    manga_name = str(choose_manga())

    parser = MangaHostParser()
    results = parser.search_for(manga_name)
    if not results:
        print("Sorry, there's no results for this search")
        exit(0)

    print("Choose the best result:\n\n")
    count = 0
    for item in results:
        print(count, "\t", item['title'])
        count += 1

    choice = None

    while True:
        choice = input(">")
        if not choice.isdigit():
            print("Incorrect answer. Try again.")
        if not results[int(choice)]:
            print("Invalid option. Try again.")
        break

    manga_name = results[int(choice)]["title"]
    manga_url = results[int(choice)]["url"]

    issues_list = parser.get_issues_list(manga_url)
    print("There are " + str(len(issues_list) + 1) + " avaliable. Choose the numbers you want")
    print("eg: 5, 6, 10-15, 23")
    print("or, if you want to download them all, type *")

    downloader = Downloader()

    choice = input(">")
    path = os.getcwd() + "\\" + manga_name + "\\"

    if choice == '*':
        for issue in issues_list:
            path = path + issue["title"] + "\\"
            for page in parser.get_pages_from_url(issue["url"]):
                 downloader.download_url(page, path)
    else:
        chosen_issues = choice.split(",")
        for chosen_issue in chosen_issues:
            issue = issues_list[int(chosen_issue)-1]
            path = path + issue["title"] + "\\"
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

            for page in parser.get_pages_from_url(issue["url"]):
                downloader.download_url(page, path)