"""module d'extraction des données du site web"""
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup, SoupStrainer
import scrapper_export as exp


DEBUG = False


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
        lien_page)  # , SoupStrainer("ol", attrs={"class": "row"})) delete

    dict_livre = {"header": {"livre_url": "product_page_url",
                             "upc": "universal_ product_code (upc)",
                             "titre": "title", "prix_ttc":  "price_including_tax",
                             "prix_ht": "price_excluding_tax", "stock": "number_available",
                             "description": "product_description", "categorie": "category",
                             "note": "review_rating", "image_url": "image_url"}}

    # determination du nombre de page à extraire dans la catégorie
    page_categorie_nombre = extract_nombre_pages_categorie(categorie_soup)

    # boucle d'extraction des pages de la catégorie
    for index_page in range(1, page_categorie_nombre + 1):
        print(nom_cat + " : extraction de la page " +
              str(index_page) + "/" + str(page_categorie_nombre))

        # chargement des pages suivantes de la catégorie lors des itérations suivantes
        if not index_page == 1:
            categorie_soup = extraction_soupe_page_lien(lien_page.replace(
                "index", "page-" + str(index_page)))

        bloc_livre_soup = categorie_soup.find_all(
            "li", {"class": re.compile("col*")})

        #boucle sur le bloc de code html d'un livre (= sur le nombre de livres de la page)
        for bloc_livre in bloc_livre_soup:
            #on recupere le lien de la page d'un livre
            livre_page_url = (
                urljoin(lien_page, str(bloc_livre.find('h3').a['href'])))

            #extraction des infos du livre traité et stockage dans un dictionaire
            info_livre = extraction_livre_info(livre_page_url, nom_cat)
            dict_livre[info_livre["titre"]] = info_livre

    #fonction de debug
    exp.export_textfile(DEBUG, output_directory,
                        "dictionnaire livres", dict_livre)

    return dict_livre


def extraction_livre_info(livre_page_url, nom_cat):
    """
    recuperation de toutes les infos d'un livre depuis la page du livre
    sous forme de dictionnaire.
    """
    page_livre_soup = extraction_soupe_page_lien(livre_page_url)

    livre_titre = str(page_livre_soup.title.get_text(strip=True)).split(
        "|", maxsplit=1)[0].strip()
    livre_upc = search_info(
        page_livre_soup, "<th>UPC</th><td>", "</td>")
    livre_prix_ht = search_info(
        page_livre_soup, "<th>Price (excl. tax)</th><td>", "</td>")
    livre_prix_ttc = search_info(
        page_livre_soup, "<th>Price (incl. tax)</th><td>", "</td>")
    livre_stock_nombre = search_info(
        page_livre_soup, "stock (", " available)")
    livre_description = str(page_livre_soup.find_all(
        'meta', attrs={'name': 'description'})).split("\"")[1].replace(r"\n", "").strip()
    livre_note = search_info(
        page_livre_soup, "star-rating ", "\">")
    livre_image_url = urljoin(
        livre_page_url, page_livre_soup.find("img")["src"])

    resultat = {"livre_url": livre_page_url, "upc": livre_upc,
                "titre": livre_titre, "prix_ttc": livre_prix_ttc,
                "prix_ht": livre_prix_ht, "stock": livre_stock_nombre,
                "description": livre_description, "categorie": nom_cat,
                "note": livre_note, "image_url": livre_image_url}

    return resultat


def search_info(texte, start, end):
    """
    on recupere le substring "texte" situé dans le code html de la page,
    situé entre les substring start et end
    """
    resultat = re.search(re.escape(start) + "(.+?)" +
                         re.escape(end), str(texte))
    if resultat:
        resultat = resultat.group(1)

    return resultat


def extract_nombre_pages_categorie(page_categorie_soup):
    """
    identification du nombre eventuel de page à l'interieur d'une categorie de livre
    a partir du soup de la premiere page
    """
    resultat = page_categorie_soup.find("li", class_="current")

    if resultat:
        resultat = str(resultat.getText()).strip().replace("Page 1 of ", "")
    else:
        resultat = 1

    return int(resultat)
