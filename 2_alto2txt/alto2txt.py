import os
import xml.etree.ElementTree as ET
from lxml import etree 
import re
import click


def process_directory(file_path, print_text, numerotation, nettoyage):
    """
    Traitement d'un XML ALTO, lancement des fonctions de renumérotation 
    ou de création de fichier txt en fonction de ce qui est demandé
    :param file_path: Chemin du fichier traité
    :param print_text: Booléen qui indique s'il est nécessaire de créer le fichier txt
    :param numerotation: Booléen qui indique s'il est nécessaire de renuméroter les fichiers ALTO
    :return: fichier txt et/ou fichier XML renuméroté et fichier txt avec les XML non traités
    """
    try:
        root, filename = os.path.split(file_path)
        if nettoyage:
            nettoyage_alto(file_path)
        if numerotation:
            update_alto_numerotation(file_path)
        if print_text or numerotation:
            xml_simple = apply_xslt(file_path)
            print_txt(root, xml_simple)
    except (ET.ParseError) as e:
        print(f'Erreur Parsage: {file_path}\n{e}')
        with open('error.txt', 'a') as f:
            f.write('Erreur Parsage:'+file_path+'\n')

def nettoyage_alto(file_path):
    """
    Supprime les lignes vides/contenant des lignes avec trop de nombres
    Si toutes les lignes d'une zone sont vides/mal formées, supprime la zone,
    :param file_path: chemin du fichier traité
    :param xml_simple: xml simplifié
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespaces = {'alto': 'http://www.loc.gov/standards/alto/ns-v4#'}
    tag = root.findall(".//alto:OtherTag", namespaces)
    number_tag_numberingzone = None
    number_tag_quiremarkzone = None
    number_tag_default = None
    for tag_line in tag:
        if tag_line.get("LABEL")=="NumberingZone":
            number_tag_numberingzone = tag_line.get("ID")
        elif tag_line.get("LABEL")=="QuiremarkZone":
            number_tag_quiremarkzone = tag_line.get("ID")
        elif tag_line.get("LABEL")=="default":
            number_tag_default = tag_line.get("ID")
    for text_block in root.findall('.//alto:TextBlock', namespaces):
        if number_tag_numberingzone or number_tag_quiremarkzone:
            tag_text_block = text_block.get("TAGREFS")
            if number_tag_numberingzone == tag_text_block or number_tag_quiremarkzone == tag_text_block:
                pass
        else:
            for line in text_block.findall('alto:TextLine', namespaces):
                liste_line_text = []
                for string in line.findall("alto:String", namespaces):
                    liste_line_text.append(string.get('CONTENT'))
                line_text = " ".join(liste_line_text)
                if len(line_text.replace(" ",""))>0:
                    numeric_char = len([char for char in line_text if char.isnumeric()])
                    majuscule_char = sum(text.isupper() for text in line_text)
                    non_alpha = '.~-+&"/()'
                    non_alpha_char = sum(line_text.count(char) for char in non_alpha)
                    if (numeric_char+non_alpha_char)/len(line_text.replace(" ",""))>0.5:
                        text_block.remove(line)
                    elif len(line_text)<3 and (numeric_char+non_alpha_char+majuscule_char)/len(line_text.replace(" ",""))>0.6:
                        text_block.remove(line)
                    elif len(line_text)==1:
                        text_block.remove(line)
                else:
                    text_block.remove(line)
    tree.write(file_path, encoding="UTF-8", xml_declaration=True)


def update_alto_numerotation(file_path):
    """
    Renumérotation des fichiers ALTO XML en suivant les numéros indiqués dans le nom du fichier
    :param: Chemin vers le fichier ALTO traité
    :return: Fichier ALTO XML renuméroté au niveau des attributs de Page
    :return: Fichier Error.txt indiquant les fichiers sans élément Page
    """
    namespace = {"alto": "http://www.loc.gov/standards/alto/ns-v4#"}
    ET.register_namespace('', namespace["alto"])
    tree = etree.parse(file_path)
    root = tree.getroot()
    pattern = re.compile(r'([0-9]*)\.xml$')
    number = re.search(pattern, file_path)
    try:
        page_number = int(number.group(1))
    except (AttributeError, ValueError) as e:
        try:
            pattern = re.compile(r'(\d+)[a-zA-Z]*(?=\.\w+$)')
            page_number = int(re.search(pattern, file_path).group(1))
        except AttributeError as e:
            page_number = 0
    page_element = root.find(".//alto:Page", namespace)
    if page_element is not None:
        id_attr = page_element.get("ID")
        if id_attr and id_attr.startswith("page_"):
            page_element.set("ID", f"page_{page_number}")
        physical_nr = page_element.get("PHYSICAL_IMG_NR")
        if physical_nr is not None:
            page_element.set("PHYSICAL_IMG_NR", str(page_number))
        tree.write(file_path, encoding="utf-8", xml_declaration=True)
    else:
        print(f"No Page element found in file: {file_path}")
        with open('error.txt', 'a') as f:
            f.write('No Page element: '+file_path+'\n')


def apply_xslt(xml_file):
    """
    Parsage d'un fichier XML ALTO et application d'une feuille XSLT de simplification
    :param xml_file: nom du fichier ALTO
    :return: ElementTree simplifié de l'ALTO
    """
    xslt_file = 'alto2XMLsimple.xsl'
    try:
        xml_tree = etree.parse(xml_file)
        xslt_tree = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_tree)
        return transform(xml_tree)
    except Exception as e:
        print(f"Error: {e}")
        return None
                

def extract_lines_from_xslt(xml_file):
    """
    Extraction du texte dans le XML ALTO simplifié
    :param xml_file: nom du fichier ALTO
    :return lines: Texte contenu dans le fichier ALTO
    :rtype: list of str
    """
    lines = []
    try:
        root = xml_file.getroot()
        # Find all <line> elements and extract their text
        for zone in root.findall(".//region"):
            for line in zone.findall(".//line"):
                if line.text:
                    lines.append(line.text.strip())
    except ET.ParseError:
        print(f"Error parsing file: {xml_file}")
    return lines


def print_txt(root, xml_file):
    """
    Création du fichier texte pour un document à partir des fichiers ALTO XML
    :param root: chemin vers le fichier ALTO
    :param xml_file: nom du fichier ALTO
    :return: fichier txt auquel est ajouté le texte contenu dans le fichier ALTO
    """
    name_file_text = f'text/{root.replace("/", "_")}.txt'
    if os.path.exists(name_file_text):
        lines = extract_lines_from_xslt(xml_file)
        with open(name_file_text, 'a') as f:
            f.write("\n".join(lines))
    else:
        lines = extract_lines_from_xslt(xml_file)
        with open(name_file_text, 'w') as f:
            f.write("\n".join(lines))


@click.command()
@click.argument('base_directory', type=str)
@click.option("-c", "--clean", "nettoyage", is_flag=True, default=False)
@click.option("-t", '--text', "print_text", is_flag=True, default=False)
@click.option("-n", "--num", "numerotation", is_flag=True, default=False)
def main(base_directory, print_text, numerotation, nettoyage):
    """
    Script permettant la renumérotation de fichiers ALTO (au niveau de la balise Page) et la production de fichiers text pour chaque document traité.
    :param base_directory: Chemin vers le dossier contenant tous les dossiers à traiter
    :param print_text: option à indiquer si l'on souhaite la génération des fichiers text (-t)
    :param numerotation: option à indiquer si l'on souhaite la renumérotation des fichiers ALTO (-n)
    """
    if not os.path.exists('text'):
        os.makedirs('text')
    for dir in sorted(os.listdir(base_directory)):
        for file_dir in sorted(os.listdir(base_directory+"/"+dir)):
            if 'xml' in file_dir:
                file_path = os.path.join(base_directory, dir, file_dir)
                print('Traitement de: '+file_path)
                process_directory(file_path, print_text, numerotation, nettoyage)
            else:
                for file in sorted(os.listdir(base_directory+'/'+dir+"/"+file_dir)):
                    file_path = os.path.join(base_directory, dir, file_dir, file)
                    print('Traitement de: '+file_path)
                    process_directory(file_path, print_text, numerotation, nettoyage)

        
if __name__ == "__main__":
    main()               
                
    

