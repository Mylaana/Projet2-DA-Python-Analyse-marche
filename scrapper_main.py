"""importation des modules requis"""
import os
import shutil
import requests
from bs4 import BeautifulSoup, SoupStrainer
import scrapper_export as exp
import scrapper_extract as ext

#debug
DEBUG = False

# constantes chemin d'acces du programme
DIRECTORY_PATH = os.path.dirname(__file__)
OUTPUT_PATH = DIRECTORY_PATH + "/Output"

#creation d'un dossier d'output
if os.path.exists(OUTPUT_PATH):
    shutil.rmtree(OUTPUT_PATH)
os.mkdir(OUTPUT_PATH)


# parsing de la page principale du site books.toscrape.com
URL_MAIN = "http://books.toscrape.com/"
reponse = requests.get(URL_MAIN, timeout=10)
page_main = reponse.content
parse_restriction = SoupStrainer("ul", attrs={"class": "nav nav-list"})
page_main_soup = BeautifulSoup(
    page_main, "html.parser", parse_only=parse_restriction)

#fonction de debug
exp.export_textfile(DEBUG, OUTPUT_PATH, "code page Accueil",
                    BeautifulSoup(page_main, "html.parser")) 


# récupération des catégories de livre depuis l'objet soup vers un dictionnaire
categorie_soup = page_main_soup.find_all("a", href=True)
dict_categorie = {}  # "nom categorie": "lien vers sa page"

for categorie in categorie_soup:
    nom_categorie = str(categorie.string).strip().replace(" ","-").lower() # pylint: disable=C0103
    if nom_categorie.upper() == "books".upper():
        continue

    for lien in page_main_soup.find_all("a"):
        if str(lien.get("href").replace(str(nom_categorie), "")).lower() != str(
                lien.get("href")).lower():
            dict_categorie[str(
                nom_categorie).replace("-"," ")] = "http://books.toscrape.com/" + lien.get("href")

#fonction de debug
exp.export_textfile(DEBUG, OUTPUT_PATH,"dictionnaire categories", dict_categorie)


# extraction et exportation des catégories de livre
for categorie, lien in dict_categorie.items():
    categorie_path = OUTPUT_PATH + "/" + categorie.upper().replace("-", " ") + "/"

    #creation d'un sous dossier d'output pour la catégorie s'il n'existe pas
    if not os.path.exists(categorie_path):
        os.mkdir(categorie_path)

    #extraction des données de la categorie
    dict_livres = ext.extraction_soupe_page_categorie(
        categorie, lien, categorie_path)

    #chargement des données dans un fichier CSV
    exp.export_csv(dict_livres, categorie, categorie_path)

    #creation d'un sous dossier d'output "IMAGE" pour la categorie
    image_path = categorie_path + "IMAGE/"
    os.mkdir(image_path)

    #chargement des images dans le dossier
    for livre_nom, livre_info  in dict_livres.items():
        if livre_nom.lower() == "header":
            continue
        exp.export_img(livre_info["image_url"], livre_info["titre"], image_path)

    print(categorie + " : terminé" )

print("end of treatments")
