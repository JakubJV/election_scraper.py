"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Jakub Vondra
email: jakubvond@seznam.cz
discord: JakubJv#7166
"""

import sys
import requests
import csv
import os
from bs4 import BeautifulSoup


def main():
    url = input_arguments()[0]
    filename = input_arguments()[1]
    header = header_scrapering(url)
    data = data_scrapering(url)
    save_to_csv(filename, header, data)
    check_file(filename)


def url_list():
    """
    List podporovaných adres pro webscrapering
    """
    main_url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    join = requests.get(main_url)
    soup = BeautifulSoup(join.text, "html.parser")
    list_href = []
    for index in range(1, 15):
        find = soup.find_all("td", {"headers": f"t{index}sa3"})
        for href in find:
            url_part = "https://volby.cz/pls/ps2017nss/"
            all_url = url_part + href.a["href"]
            list_href.append(all_url)
    return list_href


def input_arguments():
    """
    Přijímá argumet URL a název výstupního souboru.
    """
    if len(sys.argv) != 3:
        print(
            f"+--------------------------------------------------------------------------+",
            f"| 1) Jako první argument zadej URL adresu v uvozovkách:                    |",
            f'|    např.: "https://volby.cz/pls/ps2017"                                  |',
            f"| 2) Jako druhý argument zadej název souboru pro uložení dat v uvozovkách: |",
            f'|    např.: "vysledky_lipno.csv"                                          |',
            f"| 3) Celkový vzor:                                                         |",
            f"+--------------------------------------------------------------------------+",
            f'| election_scraper.py "https://volby.cz/pls/ps2017" "vysledky_lipno.csv"  |',
            f"+--------------------------------------------------------------------------+",
            sep="\n"
        )
        quit()
    elif sys.argv[2] in url_list():
        print(
            f"+--------------------------------------------------------------------------+",
            f"| Jako prní argument zadej URL adresu a jako druhý argument název souboru. |",
            f"| Argumenty zadej v uvozovkách a odděl mezerou.                            |",
            f"| Viz vzor:                                                                |",
            f"+--------------------------------------------------------------------------+",
            f'| election_scraper.py "https://volby.cz/pls/ps2017" "vysledky_lipno.csv"  |',
            f"+--------------------------------------------------------------------------+",
            sep="\n"
        )
        quit()
    elif sys.argv[1] not in url_list():
        print(
            f"+--------------------------------------------------------------------------+",
            f"| Toto URL  není podporováno.                                              |",
            f"| Zadej podporovanou URL adresu způsobem viz vzor:                         |",
            f"+--------------------------------------------------------------------------+",
            f'| election_scraper.py "https://volby.cz/pls/ps2017" "vysledky_lipno.csv"  |',
            f"+--------------------------------------------------------------------------+",
            sep="\n"
        )
        quit()
    elif not sys.argv[2].endswith('.csv'):
        print(
            f"+--------------------------------------------------------------------------+",
            f"| Název souboru musí končit příponou .csv                                  |",
            f"| Viz vzor:                                                                |",
            f"+--------------------------------------------------------------------------+",
            f'| election_scraper.py "https://volby.cz/pls/ps2017" "vysledky_lipno.csv"  |',
            f"+--------------------------------------------------------------------------+",
            sep="\n"
        )
        quit()
    else:
        url = sys.argv[1]
        filename = sys.argv[2]
    return url, filename


def header_scrapering(url):
    """
    Názvy stran z prvního odkazu stránky územních celků doplněné do hlavičky.
    """
    header = [
        "kód obce",
        "název obce",
        "voliči v seznamu",
        "vydané obálky",
        "platné hlasy",
    ]

    first_page = requests.get(url)

    print(
        f"Stahuji hlavičku z vybraného URL:",
        f"{url}",
        sep="\n"
    )

    soup = BeautifulSoup(first_page.text, "html.parser")
    first_page_href = soup.find("td", {"class": "cislo"}).a["href"]

    part_url = "https://volby.cz/pls/ps2017nss/"
    header_url = part_url + first_page_href

    second_page = requests.get(header_url)
    soup = BeautifulSoup(second_page.text, "html.parser")

    for name in (soup.find_all("td", {"class": "overflow_name"})):
        header.append(name.text)

    return header


def data_scrapering(url):
    """
    Tato funkce přidává data do listu ze stránky vybrané uživatelem. Poté přistupuje
    přes kód obce ke zbylým datům, která přidává do listu. V moment kdy má funkce
    všechna data pro danou obec, tak přidává list do listu data.
    """
    first_page = requests.get(url)

    print(
        f"Stahuji data z URL:",
        f"{url}",
        sep="\n"
    )

    soup = BeautifulSoup(first_page.text, "html.parser")

    first_page_codes = soup.find_all("td", {"class": "cislo"})
    first_page_names = soup.find_all("td", {"class": "overflow_name"})

    if len(first_page_names) == 0:
        first_page_names = soup.find_all("td", {"headers": "t1sa1 t1sb2"})

    first_page_hrefs = [href.a["href"] for href in first_page_codes]

    data = []

    part_url = "https://volby.cz/pls/ps2017nss/"

    for index, result in enumerate(first_page_hrefs, 0):
        row_list = []

        second_url = part_url + result

        second_page = requests.get(second_url)
        soup = BeautifulSoup(second_page.text, "html.parser")

        row_list.append(first_page_codes[index].text)
        row_list.append(first_page_names[index].text)

        row_list.append((soup.find("td", {"headers": "sa2"}).text).replace('\xa0', ''))
        row_list.append((soup.find("td", {"headers": "sa3"}).text).replace('\xa0', ''))
        row_list.append((soup.find("td", {"headers": "sa6"}).text).replace('\xa0', ''))

        first_candidate_parties = (soup.find_all("td", {"headers": "t1sa2 t1sb3"}))
        for data_candidate in first_candidate_parties:
            row_list.append(data_candidate.text.replace('\xa0', ''))

        second_candidate_parties = (soup.find_all("td", {"headers": "t2sa2 t2sb3"}))
        for data_candidate in second_candidate_parties:
            numeric = (data_candidate.text.replace('\xa0', ''))
            if numeric.isnumeric():
                row_list.append(numeric)

        data.append(row_list)

    return data


def check_file(filename):
    dash = "-" * len(filename)

    if filename in os.listdir():
        print(
            f"+---------------------------{dash}+",
            f"| Data uložena do souboru: {filename} |",
            f"+---------------------------{dash}+",
            f"Ukončuji program...",
            sep="\n", end=("")
        )
    else:
        print(
            f"+--------------------{dash}+",
            f"| Soubor nenalezen: {filename} |",
            f"+--------------------{dash}+",
            f"Ukončuji program...",
            sep="\n", end=("")
        )


def save_to_csv(filename, header, data):
    """
    Uloží data do csv souboru.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as data_csv:
        writer = csv.writer(data_csv)
        print(
            f"Ukládám data do vybraného souboru:",
            f"{filename}",
            sep="\n"
        )
        writer.writerow(header)
        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    main()
