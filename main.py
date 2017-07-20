# -*- coding: utf-8 -*-
import os

from tabulate import tabulate

from progress import progress
from mhdownloader import MangaHostDownloader
from mhparser import MangaHostParser


def choose_manga():
    choice = None
    while not choice:
        choice = input("Qual mangá você busca? > ")
    return choice

if __name__ == '__main__':

    print('------------------ MangaHost Downloader -------------------')
    print('|Esse programa foi criado apenas para fins de aprendizagem|')
    print('-----------------------------------------------------------')
    print('\n')

    manga_name = str(choose_manga())

    parser = MangaHostParser()
    results = parser.search_for(manga_name)
    if not results:
        print("Não há resultados para essa busca.")
        exit(0)

    print("Resultados da busca:\n")
    count = 0
    tab_results = []
    for item in results:
        tab_results.append([count, item['title']])
        count += 1

    print(tabulate(tab_results, headers=['#', 'Título'], tablefmt='orgtbl'))
    print()
    choice = None

    while True:
        choice = input("Digite o tem desejado: >")
        if not choice.isdigit():
            print("Opção inválida. Tente novamente.")
            continue
        if not results[int(choice)]:
            print("Opção inválida. Tente novamente.")
            continue
        break

    manga_name = results[int(choice)]["title"]
    manga_url = results[int(choice)]["url"]

    issues_list = parser.get_issues_list(manga_url)
    print("Esse mangá possui " + str(len(issues_list)) + " edições disponíveis.")
    print("Digite as edições que deseja separadas por vírgula.")
    print("\tExemplo: 5, 6, 10-15, 23")
    print("Caso deseje todas, digite *")

    mhdownloader = MangaHostDownloader()

    choice = input(">")
    base_path = os.getcwd() + "\\" + manga_name + "\\"

    if choice == '*':
        for issue in issues_list:
            path = base_path + issue["title"] + "\\"
            for page in parser.get_pages_from_url(issue["url"]):
                 mhdownloader.download_url(page, path)
    else:
        chosen_issues = choice.split(",")

        for chosen_issue in chosen_issues:
            issue = issues_list[int(chosen_issue)-1]
            path = base_path + issue["title"] + "\\"
            pages_list = parser.get_pages_from_url(issue["url"])
            for idx, page in enumerate(pages_list):
                progress(idx + 1, len(pages_list), issue["title"])
                mhdownloader.download_url(page, path)