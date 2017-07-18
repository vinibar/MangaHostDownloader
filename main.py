# -*- coding: utf-8 -*-
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
        choice = input()
        if not choice.isdigit():
            print("Incorrect answer. Try again.")
        if not results[int(choice)]:
            print("Invalid option. Try again.")
        break

    for issue in parser.get_issues_list(results[int(choice)]["url"]):
        print(issue)