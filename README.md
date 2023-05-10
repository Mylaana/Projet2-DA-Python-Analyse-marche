# Projet2-DA-Python-analyse-marche
## 1 - Création de l'environnement virtuel

Ouvrez un terminal sur votre système d'exploitation. Assurez-vous que **Python est installé** en tapant la commande suivante :
```
python --version
```

Si Python n'est pas installé, vous pouvez le télécharger sur le site web officiel de Python :  
https://www.python.org/downloads/

Dans le terminal, naviguez vers le dossier dans lequel vous souhaitez installer un environnement virtuel à l'aide de la commande :
```
cd disque/mon/chemin/
```


Installez le module venv en tapant la commande suivante dans le terminal :
```
python -m venv myenv
```

Cette commande crée un environnement virtuel nommé "myenv". Vous pouvez remplacer "myenv" par le nom de votre choix.

## 2 - Activation de l'environnement virtuel

**Activez l'environnement virtuel** en tapant la commande suivante :

Sous **Windows** :
```
myenv\Scripts\activate.bat
```

Sous **Linux / MacOS** :
```
source myenv/bin/activate
```

Une fois l'environnement virtuel activé, le terminal renvoie une ligne commençant par le nom de l'environnement entre parenthèses, du type :
```
(myenv) disque/mon/chemin
```


Pour **quitter l'environnement virtuel**, tapez simplement la commande suivante :
```
deactivate
```

## 3 - Installation des packages et lancement de l'application

Une fois l'environnement virtuel **créé et activé**, naviguez vers le dossier dans lequel se situe le script à lancer  
(s'il n'était pas dans le même dossier que l'environnement virtuel).

Installez les packages nécessaires au fonctionnement du script à l'aide de la commande : 
```
pip install -r requirements.txt
```

Une fois l'installation terminée, lancez le script : 
```
python scrapper_main.py
```

Le script affichera dans le terminal sa progression, et aura terminé une fois le message **end of treatments** affiché.
