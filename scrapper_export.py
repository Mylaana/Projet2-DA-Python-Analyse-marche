"""module contenant les fonctions d'exportation"""
import shutil
import csv
import requests

DEBUG = False

# export * to text file
def export_textfile(debug, directory, textfile_name, text_value):  
    """fonction d'exportation de fichier texte a l'emplacement désigné"""
    if not debug:
        return None
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

def export_csv(data: dict, nom_fichier_csv: str, save_path: str):
    """exportation d'un dictionnaire de donnée en format CSV"""

    with open(save_path + nom_fichier_csv + ".csv", "w",encoding="utf-8") as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=",")
        for ligne in data:
            writer.writerow(data[ligne].values())

def export_img(image_url: str, image_nom: str, save_path: str):
    """
    exportation d'une image à partir du lien, vers le dossier spécifié
    """
    res = requests.get(image_url, stream = True, timeout= 10)
    image_extension = "." + image_url.split(R".")[-1]

    if res.status_code == 200:
        with open(save_path + image_nom + image_extension,'wb') as f:
            shutil.copyfileobj(res.raw, f)
    else:
        print("could not download image : " + image_nom)
