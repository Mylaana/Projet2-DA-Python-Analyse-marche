"""importation des modules"""
import re

def no_char_spe(ma_chaine: str):
    """
    suppression des caracteres speciaux

    resultat = re.sub("[!@#$%^&*()[]{};:,./<>?\|`~-=_+]", "", ma_chaine)
    resultat = resultat.replace(".", "").replace(",", "").replace(":",""
                        ).replace("(","").replace(")","").replace("#",""
                        ).replace("/","").replace("\\","")
    """
    resultat = re.sub(r"[^a-zA-Z0-9\s-]", "", ma_chaine)
    
    return resultat
