"""importation des modules"""
import re
from urllib.parse import urljoin

def no_char_spe(ma_chaine: str):
    """
    suppression des caracteres speciaux
    """
    resultat = re.sub(r"[^a-zA-Z0-9\s-]", "", ma_chaine)

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


def transform_livre_info(livre_page_url, nom_cat, page_livre_soup):
    """
    recuperation de toutes les infos d'un livre depuis la page du livre
    sous forme de dictionnaire.
    """

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
