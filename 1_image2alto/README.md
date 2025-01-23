# Image2ALTO

Ce script python permet de transformer les images numérisés de documents en fichiers ALTO en employant la librairie python Release the Kraken (RTK) de management de tâches. Il permet:

- l'analyse de la mise en page pour chaque image (reconnaitre les titres, paragraphes, images, etc....) en utilisant un modèle YOLO [LADaS](https://github.com/DEFI-COLaF/LADaS)
- la transcription automatique du contenu textuel de ces pages en utilisant [kraken](https://kraken.re/) comme logiciel d'OCR et un modèle [CATMuS](https://zenodo.org/records/10592716)

## Guide d'utilisation
GPU nécessaire.

- Git clone le projet
- Récupérer les dernières versions du modèle ladas pour l'analyse de la mise en page. Télécharger le modèle Catmus nécessaire (Print si imprimé moderne, gothic etc...)
- Installer RTK en suivant les informations [ici](https://github.com/PonteIneptique/RTK) dans le dossier
- Changer le lien vers les modèles dans le script (L16 et L37 dans rtk_bis.py)
- installer l'environnement virtuel python3 -m venv venv-image2alto, source venv-image2alto/bin/activate, et installer les requirements pip3 install -r requirements.txt
- Création des batchs: python3 creation_csv_batch.py [nom_dossier_image]
- Vérifier que le csv image_batch.csv a été créé
- Lancer sh batch_process.sh
