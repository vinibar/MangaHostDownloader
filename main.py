# -*- coding: utf-8 -*-
from manga_downloader import MangaHostParser

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

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




