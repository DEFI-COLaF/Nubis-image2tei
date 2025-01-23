# ALTO2txt

Ce script python permet la renumérotation de fichiers ALTO XML et la génération du texte contenu dans ces fichiers dans des fichiers txt.

Le script s'utilise sur des fichiers ALTO XML contenus dans un dossier principal [Dossier_contenant]. L'option renumérotation permet d'aligner la numérotation dans la balise Page à celle indiquée dans le nom du fichier. Le fichier texte produit correspond aux transcriptions contenues dans les fichiers ALTO d'un document, matérialisé par un dossier par document. Un fichier exemple est disponible si besoin.

## Guide d'utilisation
  - Cloner le dépôt sur sa machine: ```git clone https://github.com/DeFI-COLaF/alto2txt``` et rentrer dans le dossier créé (```cd alto2txt```)
  - Créer l'environnement: ```python3 -m venv venv-alto```
  - Lancer l'environnement: ```source env-alto/bin/activate```
  - Installer les librairies nécessaires: ```pip install -r requirements.txt```
  - Lancer l'application: ```python3 alto2txt.py [Dossier_contenant] -t -n```
  Si l'on souhaite uniquement la génération des textes, conserver le ```-t``` des deux options, si l'on souhaite uniquement la rénumérotation des fichiers ALTO, conserver le ```-n``` uniquement, ``-c``` pour un nettoyage minimal du corpus (suppression des éléments bruités avec trop de majuscules, de chiffres ou de caractères non alphabétiques).
- Arrêter l'environnement: ```source env/bin/deactivate```
