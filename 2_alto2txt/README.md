# ALTO2txt

Ce script python permet la renumérotation de fichiers ALTO XML et la génération du texte contenu dans ces fichiers dans des fichiers txt.

Le script s'utilise sur des fichiers ALTO XML contenus dans un dossier principal [Dossier_contenant]. L'option renumérotation permet d'aligner la numérotation dans la balise Page à celle indiquée dans le nom du fichier. Le fichier texte produit correspond aux transcriptions contenues dans les fichiers ALTO d'un document, matérialisé par un dossier par document. Un fichier exemple est disponible si besoin.

## Guide d'utilisation

### Prérequis
Si non fait:
  1. ***Cloner le dépôt*** sur sa machine: ```git clone https://github.com/DeFI-COLaF/alto2txt```

  2. ***Créer l'environnement***: ```python3 -m venv venv-alto2txt```
  3. ***Lancer l'environnement***: ```source env-alto/bin/activate```
  4. ***Installer les librairies*** nécessaires: ```pip install -r requirements.txt```

### Lancement de l'application
Chaque tâche a été construite comme une option à ajouter à la commande en fonction du besoin:

- ```-n```: renumérotation des fichiers ALTO
- ```-c```: nettoyage minimal du corpus (suppression des éléments bruités avec trop de majusucules, de chiffres ou de caractères non alphabétiques)
- ```-t```: génération des fichiers txt avec le contenu textuel de chaque document - 1 document = 1 dossier avec des ALTO

Exemples de commande:
- ```python3 alto2txt.py [Dossier_contenant] -t```: génération de texte uniquement
- ```python3 alto2txt.py [Dossier_contenant] -t -c```: génération de texte et nettoyage minimal du corpus
- ```python3 alto2txt.py [Dossier_contenant] -t -c -n```: toutes les options
