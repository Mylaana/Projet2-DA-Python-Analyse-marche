"""importation des modules requis"""
import os
import requests
from bs4 import BeautifulSoup, SoupStrainer
import scrapper_export as exp
import scrapper_extract as ext

# set up
DEBUG = False

DIRECTORY_PATH = os.path.dirname(__file__)
OUTPUT_PATH = DIRECTORY_PATH + "/Output"
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)


# lien de la page à scrapper
URL_MAIN = "http://books.toscrape.com/"
reponse = requests.get(URL_MAIN, timeout=10)
page_main = reponse.content
exp.export_textfile(DEBUG, OUTPUT_PATH, "code page Accueil",
                    BeautifulSoup(page_main, "html.parser"))

# transforme (parse) le HTML en objet BeautifulSoup
parse_restriction = SoupStrainer("ul", attrs={"class": "nav nav-list"})
page_main_soup = BeautifulSoup(
    page_main, "html.parser", parse_only=parse_restriction)

# récupération des catégories de livre
categorie_soup = page_main_soup.find_all("a", href=True)
dict_categorie = {}  # "nom categorie": "lien vers sa page"
for categorie in categorie_soup:
    nom_categorie = str(categorie.string).strip().lower().replace(
        " ", "_")  # pylint: disable=C0103
    if nom_categorie.upper() == "books".upper():
        continue

    for lien in page_main_soup.find_all("a"):
        if str(lien.get("href").replace(str(nom_categorie), "")).lower() != str(
                lien.get("href")).lower():
            dict_categorie[str(
                nom_categorie)] = "http://books.toscrape.com/" + lien.get("href")

exp.export_textfile(DEBUG, OUTPUT_PATH,
                    "dictionnaire categories", dict_categorie)


# extraction de catégorie de livre
for categorie, lien in dict_categorie.items():
    # todel to del quand on bouclera sur toutes les cat

    categorie_path = OUTPUT_PATH + "/" + categorie.upper() + "/"
    if categorie != "fantasy":

        continue

    if not os.path.exists(categorie_path):
        os.mkdir(categorie_path)

    dict_livres = ext.extraction_soupe_page_categorie(
        categorie, dict_categorie[categorie], categorie_path)
    exp.export_csv(dict_livres, categorie, categorie_path)
