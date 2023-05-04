"""module d'extraction des données du site web"""
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup, SoupStrainer
import scrapper_export as exp


DEBUG = True


def extraction_soupe_page_lien(lien_page: str, parse_only: SoupStrainer = None):
    """extraction & parsing d'une page"""
    reponse = requests.get(lien_page, timeout=10)
    page_categorie = reponse.content
    resultat_soup = BeautifulSoup(
        page_categorie, "html.parser", parse_only=parse_only)

    return resultat_soup


def extraction_soupe_page_categorie(nom_cat, lien_page, output_directory):
    """
    fonction d'extraction d'une catégorie de livre
    recuperation du code de la page, parsing,
    puis traitement de chaque bloc de code html de livre
    """
    categorie_soup = extraction_soupe_page_lien(
        lien_page, SoupStrainer("ol", attrs={"class": "row"}))
    bloc_livre_soup = categorie_soup.find_all(
        "li", {"class": re.compile("col*")})

    exp.export_textfile(DEBUG, output_directory,
                        "parsing " + nom_cat, categorie_soup)
    exp.export_textfile(DEBUG, output_directory, "parsing " +
                        nom_cat + "findall", str(bloc_livre_soup))

    dict_livre = {}  # ensemble des informations des livres de la catégorie
    for bloc_livre in bloc_livre_soup:
        livre_page_url = (
            urljoin(lien_page, str(bloc_livre.find('h3').a['href'])))
        page_livre_soup = extraction_soupe_page_lien(livre_page_url)

        livre_titre = str(page_livre_soup.title.get_text(strip=True)).split(
            "|", maxsplit=1)[0].strip()
        livre_upc = extraction_livre_info(
            page_livre_soup, "<th>UPC</th><td>", "</td>")
        livre_prix_ht = extraction_livre_info(
            page_livre_soup, "<th>Price (excl. tax)</th><td>", "</td>")
        livre_prix_ttc = extraction_livre_info(
            page_livre_soup, "<th>Price (incl. tax)</th><td>", "</td>")
        livre_stock_nombre = extraction_livre_info(
            page_livre_soup, "stock (", " available)")
        livre_description = str(page_livre_soup.find_all(
            'meta',attrs={'name':'description'})).split("\"")[1].replace(r"\n","").strip()
        livre_note = extraction_livre_info(
            page_livre_soup, "star-rating ","\">")
        livre_image_url = urljoin(livre_page_url,page_livre_soup.find("img")["src"])

        dict_livre = {livre_titre: {"livre_url": livre_page_url, "upc": livre_upc,
                                    "prix_ht":  livre_prix_ht, "prix_ttc": livre_prix_ttc,
                                    "stock": livre_stock_nombre,"description": livre_description,
                                    "categorie": nom_cat, "note": livre_note,
                                    "image_url": livre_image_url}}

    exp.export_textfile(DEBUG, output_directory,
                    "dictionnaire livres", dict_livre)

    return dict_livre

def extraction_livre_info(page_livre_soup, start, end):
    """
    on recupere le substring situé dans le code html de la page,
    situé entre les substring start et end
    """
    resultat = re.search(re.escape(start) + "(.+?)" +
                         re.escape(end), str(page_livre_soup))
    if resultat:
        resultat = resultat.group(1)
    else:
        print(resultat)
    return resultat
