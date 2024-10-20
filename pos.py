import re
import chardet
import spacy
import tempfile

# Fonction pour nettoyer le texte d'un fichier
def nettoyer_texte(fichier_txt):
    # Détection automatique de l'encodage
    with open(fichier_txt, 'rb') as f:
        resultat = chardet.detect(f.read())
        encodage = resultat['encoding']

    # Lire le fichier avec l'encodage détecté
    with open(fichier_txt, 'r', encoding=encodage) as f:
        texte = f.read()

    # Chercher les deux formats possibles pour supprimer la première page (2 ou -2-)
    index_fin_premiere_page = texte.find('-2-')  # D'abord chercher le format "-2-"
    if index_fin_premiere_page == -1:  # Si format "-2-" non trouvé, chercher " 2"
        index_fin_premiere_page = texte.find('2')

    if index_fin_premiere_page != -1:
        # Supprimer tout avant et y compris la première page
        if texte[index_fin_premiere_page:index_fin_premiere_page+len('-2-')] == '-2-':
            texte = texte[index_fin_premiere_page + len('-2-'):]  # Supprimer "-2-"
            texte = re.sub(r'-\s*\d+\s*-', '', texte)
        elif texte[index_fin_premiere_page:index_fin_premiere_page+len('2')] == '2':
            texte = texte[index_fin_premiere_page + len('2'):]  # Supprimer " 2"
            texte = re.sub(r'\d+\s', '', texte)  # Remplacer les numéros de page du type " X " par un espace

    # Supprimer les nombres romains (par exemple, I, II, III, IV, V, VI, etc.)
    texte = re.sub(r'[IVXLCDM]+\s', '', texte)  # Supprimer les nombres romains suivis d'un espace

    return texte

# Fonction pour effectuer l'analyse POS avec SpaCy
def spacy_pos_tag(text):
    # Charger le modèle français
    nlp = spacy.load("fr_core_news_md")
    doc = nlp(text)
    
    # Créer une liste de tuples (mot, POS)
    return [(token.text, token.pos_) for token in doc]

# Fonction pour écrire les résultats dans un fichier
def ecrire_texte_et_pos(fichier_sortie, texte_nettoye, pos_tags):
    with open(fichier_sortie, 'w', encoding='utf-8') as f_sortie:
        for token, pos in pos_tags:
            f_sortie.write(f"{token}/{pos} ")
        f_sortie.write("\n\nTexte original nettoyé :\n\n")
        f_sortie.write(texte_nettoye)

# Utilisation
fichier_txt = 'Fondation_et_empire_sample.txt'  # Fichier d'entrée (texte brut)
fichier_sortie = 'Fondation_et_empire_sample_sortie.txt'  # Fichier de sortie

# Nettoyer le texte
texte_propre = nettoyer_texte(fichier_txt)

# Analyser le texte avec SpaCy pour obtenir les POS tags
tags = spacy_pos_tag(texte_propre)

# Écrire le texte nettoyé et les POS dans le fichier de sortie
ecrire_texte_et_pos(fichier_sortie, texte_propre, tags)

print(f"Le fichier {fichier_sortie} a été généré avec le texte nettoyé et les étiquettes POS.")
