Election Scraper

Jedná se o Třetí projekt zpracovaný v rámci zadání Engeto Akademie.

Popis projektu
Tento projekt slouží ke stahování výsledků voleb konaných v roce 2017 do souboru .csv. 

Instalace
postup je popsán pro OS Windows a prostředí IDE PyCharm.
Instalace virtuálního prostředí
Pro instalaci knihoven doporučuji vytvořit ve složce s projektem virtuální Python prostředí. 
Virtuální prostředí si vytvoříme při tvorbě projektu přímo v PyCharmu, kde v záložce "New enviroment using" zaškrtneme Virtualenv.

Poté si můžete povšimnout, že se vám v projektu vytvořil soubour venv, což značí úspěšné vytvoření virtuálního prostředí. 

Absolutní cesta zavisí na vaší konfiguraci (uživatelské jméno, umístění složky,...).

Dále si nainstalujeme soubour requirements.txt se seznamem použitých knihoven. 
Tento soubor vytvoříme tak, že v záložce v IDE PyCharm (Tools) zvolíme možnost Sync Python Requirements.

Poté se vám objeví textový soubor, který je prozatím prázdný, ale v jeho vrchní části si poté povšimnete možnosti "Add imported packages to requirements, kterou zvolíte
a v ten moment budete mít v tomto soubouru jména všech dostupných knihoven.



Spuštění projektu
Spuštění souboru election_scraper.py v terminálu resp. v příkazovém řádku v PyCharm požaduje zadat dva argumenty v následujícím pořadí:

Nejdříve odkaz vybrané webové stránky ze které chceme data stahovat a poté zadat název výsledného souboru s příponou ".csv".
Např. takto:

python election_scraper.py <"okdaz_webu"> <"vysledny_soubor">
Výstupem programu bude soubor se staženými daty ve formátu .csv.
Úplně přesně vás vstup má vypadat takto:

python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=6&xnumnuts=4204" "vysledky_lipno.csv"
