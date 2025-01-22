# Chaîne de traitement de l'image au texte appliqué à la NuBIS

Ce dépôt a été produit dans le cadre d'une collaboration entre la Bibliothèque interuniversitaire de la Sorbonne ([Nubis](https://www.bis-sorbonne.fr/nubis)) et le projet [COLAF](https://colaf.huma-num.fr), géré par l'équipe projet [ALMAnaCH](https://team.inria.fr/almanach/) de l'[Inria](https://www.inria.fr).

## Objectif
Le projet traite des monographies et autres textes numérisés par la BIS, couvrant des documents du 15ème au 20ème siècle dans plusieurs langues (latin, français, italien, espagnol, par ordre d'importance). Ce dépôt contient les scripts développés pour :

- Transformer les images numérisées des documents en fichiers ALTO XML.
- Renuméroter et nettoyer les fichiers ALTO XML obtenus selon les souhaits de la Nubis.
- Générer une version texte du contenu textuel de chaque document, répondant aux besoins spécifiques de Nubis.

## Contenu du dépôt

### 1. Dossier `1_image2alto`
Ce dossier contient les scripts utilisés pour générer des fichiers ALTO XML à partir des images numérisées via la librairie python **[Release the Kraken (RTK)](https://kraken.re/)**.

### 2. Dossier `2_alto2txt`
Ce dossier contient un script Python conçu pour nettoyer et renuméroter les fichiers ALTO XML selon les spécifications de Nubis et générer un fichier texte contenant le contenu textuel de chaque document.

## Licence
![Licence CC-BY](https://licensebuttons.net/l/by/4.0/88x31.png)

Les scripts de ce dépôt sont librement réutilisables et adaptables sous licence [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Contact
Pour toute question ou demande, n'hésitez pas à consulter les contacts et informations dans la documentation.
