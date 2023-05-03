"""module contenant les fonctions d'extraction des categories de livre"""
import requests
from bs4 import BeautifulSoup

DEBUG = False

# export * to text file
def export_textfile(debug, directory, textfile_name, text_value):  
    """fonction d'exportation de fichier texte a l'emplacement désigné"""
    if not debug:
        return
    textfile_name = "export - " + textfile_name.lower()
    with open(str(directory + "/").replace("//", "/") +
              textfile_name.replace(".txt", "") + ".txt",
              mode="w", encoding="utf-8") as output_textfile:
        print("export : " + textfile_name + " as " + str(type(text_value)))
        if isinstance(text_value, dict) or isinstance(text_value, list):
            for line in text_value.items():
                output_textfile.write(str(line) + "\n")
        else:
            output_textfile.write(str(text_value))

# fonction d'extraction d'une catégorie de livre
def extraction_categorie_livre(nom_cat, lien_page, output_directory): 
    """recuperation du code de la page, parsing, puis export sous format CSV"""
    # print(nom_cat + ": " + lien_page)
    reponse = requests.get(lien_page, timeout=10)
    page_categorie = reponse.content
    export_textfile(DEBUG, output_directory, "parsing "+ nom_cat,
                    BeautifulSoup(page_categorie, "html.parser"))
    

#limiter parsing a "OL class= row"
