# Image2ALTO

Ce script python permet de transformer les images numérisés de documents en fichiers ALTO en employant la librairie python Release the Kraken (RTK) de management de tâches. Il permet:

- l'analyse de la mise en page pour chaque image (reconnaitre les titres, paragraphes, images, etc....) en utilisant un modèle YOLO [LADaS](https://github.com/DEFI-COLaF/LADaS)
- la transcription automatique du contenu textuel de ces pages en utilisant [kraken](https://kraken.re/) comme logiciel d'OCR et un modèle [CATMuS](https://zenodo.org/records/10592716)

## Guide d'utilisation

### Prérequis

Ce projet nécessite l'utilisation d'un GPU.

1. ***Cloner le dépôt github*** :  ```git clone https://github.com/DEFI-COLaF/Nubis-image2txt```
2. ***Installer Release the Kraken***: Cloner le dépôt RTK dans le dossier Nubis-image2txt
  - ```cd Nubis image2txt```
  - ```git clone https://github.com/PonteIneptique/rtk```
3. ***Télécharger les modèles nécessaires***:
- Dernière version du modèle LADaS pour l'analyse de la mise en page: https://github.com/DEFI-COLaF/LADaS/releases
- Modèle CATMuS le plus adéquat pour les données à traiter
- Les ajouter dans le dossier Nubis-image2txt
4. ***Modifier les scripts***:Pour pointer vers les modèles téléchargés
- Ligne 16 de ```RTK_bis.py```: remplacer le chemin par le chemin vers le modèle LADaS
- Ligne 27 de ```RTK_bis.py```: remplacer le chemin par le chemin vers le modèle CATMuS
5. ***Générer un fichier CSV*** listant les images à traiter et les divisant en batch:
   ```python3 creation_csv_batch.py [nom_du_dossier_image]```
6. ***Créer un fichier ```status_bis.txt```*** qui contient 0

### Installation des dépendances
1. ***Créer un environnement virtuel***: ```python3 -m venv venv-image2alto```
2. ***Installer les dépendances spécifiques à RTK***: se référer aux informations fournies sur le dépôt de la librairie 
3. ***Installer la dépendance spécifique à image2txt***: ```pip3 install click```

### Lancement
1. ***Vérifier que le programme fonctionne***: ```sh batch_process.sh```
2. ***Ouvrir le crontab*** pour relancer le programme automatiquement pour chaque batch:
   ```crontab -e```
3. ***Ajouter la ligne***:
   ```*/4 * * * * sh [chemin vers batch_process.sh] >> crontab_log.log 2<&1```
   
Toutes les quatre minutes, le programme va vérifier si un job est déjà en cours et si non, en lancer un nouveau (batch_process.sh). Un job correspond au traitement d'un lot de 200 images (dans rtk_bis.py), chacun étant numéroté (le numéro traité sur le moment est dans status_bis.txt). Les logs de lancement sont disponibles dans le fichier crontab_log.log et les logs de chaque job dans un dossier logs. Il faut supprimer le crontab quand toutes les images ont été traitées.

   
