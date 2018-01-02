# -*- coding: utf-8 -*-
import os
import zipfile
import shutil

from tabulate import tabulate

from progress import progress
from mhdownloader import MangaHostDownloader
from mhparser import MangaHostParser
from requests.utils import requote_uri


def choose_manga():
    choice = ""
    while choice.strip() == "":
        choice = input("Qual mangá você busca? > ")
    return choice

if __name__ == '__main__':

    print('------------------ MangaHost Downloader -------------------')
    print('|   Download de Mangás diretamente do site MangaHost.com  |')
    print('-----------------------------------------------------------')
    print('\n')

    manga_name = str(choose_manga())

    parser = MangaHostParser()
    try:
        results = parser.search_for(manga_name)
    except AttributeError:
        print("Não há resultados para essa busca.")
        exit(0)

    print("\n\nResultados da busca:\n")
    count = 0
    tab_results = []
    for item in results:
        tab_results.append([count, item['title']])
        count += 1

    print(tabulate(tab_results, headers=['#', 'Título'], tablefmt='orgtbl'))
    print()
    choice = None

    while True:
        choice = input("Digite o item desejado: >")
        if not choice.isdigit():
            print("Opção inválida. Tente novamente.")
            continue
        if not results[int(choice)]:
            print("Opção inválida. Tente novamente.")
            continue
        break

    manga_name = results[int(choice)]["title"]
    manga_url = results[int(choice)]["url"]

    issues_list, special_list = parser.get_issues_list(manga_url)
    print("Esse mangá possui " + str(len(issues_list)) + " edições disponíveis.")
    print("Sendo " + str(len(special_list)) + " especiais (últimas da lista)")
    print("Para listar todas, digite `list`")
    print("Digite as edições que deseja separadas por vírgula.")
    print("\tExemplo: 5, 6, 10-15, 23")
    print("Para baixar todas, digite *")

    mhdownloader = MangaHostDownloader()

    while True:
        choice = input(">")
        base_path = os.getcwd() + "\\" + manga_name + "\\"

        if choice == '*':
            for issue in issues_list:
                path = base_path + issue["title"] + "\\"
                pages_list = parser.get_pages_from_url(issue["url"])
                for idx, page in enumerate(pages_list):
                    progress(idx + 1, len(pages_list), issue["title"])
                    mhdownloader.download_url(page, path)
                print()
            exit(0)
        elif choice == 'list':
            tab_results = []
            count = 1
            for issue in issues_list:
                tab_results.append([count, issue['title']])
                count += 1
            print(tabulate(tab_results, headers=['#','Título'], tablefmt='orgtbl'))
        else:
            chosen_issues = choice.split(",")

            for chosen_issue in chosen_issues:

                if not str(chosen_issue).isdigit():
                    interval = [int(i) for i in chosen_issue.split('-')]
                    if len(interval) <= 1:
                        print(chosen_issue + " é uma opção inválida e será descartada.")
                        continue
                    [chosen_issues.append(x) for x in list(range(interval[0], interval[1]+1))]
                    continue

                try:
                    issue = issues_list[int(chosen_issue)-1]
                except IndexError:
                    print(chosen_issue + " é uma opção inválida e será descartada.")
                    continue

                path = base_path + issue["title"] + "\\"
                pages_list = parser.get_pages_from_url(issue["url"])
                print("Edição: ", issue["title"])
                print("Quantidade de paginas: ", len(pages_list))
                for idx, page in enumerate(pages_list):
                    progress(idx + 1, len(pages_list), issue["title"])
                    mhdownloader.download_url(requote_uri(page), path)

                zip_path = base_path + issue["title"] + '.cbz'
                zipf = zipfile.ZipFile(zip_path, 'w')
                for file in os.listdir(path):
                    # remove white borders
                    fp = os.path.join(path, file)
                    parser.remove_borders(fp)
                    zipf.write(fp, os.path.relpath(os.path.join(path, file), path), compress_type=zipfile.ZIP_DEFLATED)
                zipf.close()
                shutil.rmtree(path)