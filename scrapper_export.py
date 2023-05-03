"""module contenant les fonctions d'exportation"""
import csv

DEBUG = True

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
