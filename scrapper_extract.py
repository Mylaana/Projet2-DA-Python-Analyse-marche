"""module d'extraction des données du site web"""
import requests
from bs4 import BeautifulSoup, SoupStrainer
import scrapper_export as exp

DEBUG = True

# fonction d'extraction d'une catégorie de livre
def extraction_categorie_livre(nom_cat, lien_page, output_directory): 
    """recuperation du code de la page, parsing, puis export sous format CSV"""
    # print(nom_cat + ": " + lien_page)
    reponse = requests.get(lien_page, timeout=10)
    page_categorie = reponse.content
    parse_restriction = SoupStrainer("ol", attrs={"class": "row"})
    exp.export_textfile(DEBUG, output_directory, "parsing "+ nom_cat,
                    BeautifulSoup(page_categorie, "html.parser", parse_only=parse_restriction))
