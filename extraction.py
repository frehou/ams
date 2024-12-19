import stanza
import networkx as nx
import pandas as pd
import os
import re
from flair.models import SequenceTagger
from flair.data import Sentence

# Charger le modèle Flair pour la reconnaissance d'entités nommées
flair_tagger = SequenceTagger.load("flair/ner-english-large")


# Charger un modèle pré-entraîné pour la reconnaissance des entités nommées
stanza.download('fr')
nlp = stanza.Pipeline('fr')
dictionary_path = "antidic.txt"

def load_dictionary(file_path):
    """
    Charge un dictionnaire de mots fonctionnels à partir d'un fichier.
    Retourne un ensemble pour des comparaisons rapides.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        dictionary = set(line.strip().lower() for line in f if line.strip() and not line.startswith('#'))
    return dictionary

def extract_characters(text):
    """
    Extrait les personnages (entités nommées de type PERSON) d'un texte.
    """
    french_dictionary = load_dictionary(dictionary_path)

    # Détecter les personnages avec Stanza
    doc = nlp(text)
    characters = [ent.text for sentence in doc.sentences for ent in sentence.ents if ent.type == "PER" and ent.text.lower() not in french_dictionary and len(ent.text) > 2]
    

    # Détecter les lieux avec Flair
    loc = []
    flair_sentence = Sentence(text)
    flair_tagger.predict(flair_sentence)
    for entity in flair_sentence.get_spans("ner"):
        if entity.tag == "LOC":
            loc.append(entity.text)

    names = []
    for name in characters:
        cleaned_name = re.sub(r'\s+', ' ', name).replace('\n', ' ').strip()

        if cleaned_name not in names and cleaned_name not in loc:
            names.append(cleaned_name)

   
    return names

def group_names(names_list):
    """
    Alias: regrouper les noms des personnages.
    """

    stop_words = {"mr", "m", "mme", "ms", "dr", "r", "sere", "sire", "sir"}

    groups = []
    seen = set()

    for name in names_list:
        if name in seen:
            continue

        current_group = [name]
        seen.add(name)
        added = True

        while added:
            added = False
            for other_name in names_list:
                if other_name in seen:
                    continue

                for group_name in current_group:
                    name_parts = group_name.split()
                    other_name_parts = other_name.split()

                    if len(name_parts) == 2 and len(other_name_parts) == 2:
                        if ((name_parts[0].lower() in stop_words) or (other_name_parts[0].lower() in stop_words)) and ((name_parts[1].lower() in other_name.lower()) or (other_name_parts[1].lower() in group_name.lower())):
                            current_group.append(other_name)
                            seen.add(other_name)
                            added = True
                            break

                        if name_parts[0].lower() == other_name_parts[0].lower() and \
                           name_parts[1].lower() == other_name_parts[1].lower():
                            current_group.append(other_name)
                            seen.add(other_name)
                            added = True
                            break
                        else:
                            break

                    elif group_name.lower() in other_name.lower() or other_name.lower() in group_name.lower():
                        current_group.append(other_name)
                        seen.add(other_name)
                        added = True
                        break

        groups.append(current_group)

    return groups

def create_chapter_graph(chapter_text, window_size=25):
    """
    Crée un graphe de personnages pour un chapitre donné en utilisant des co-occurrences.
    """
    # Extraire les personnages
    characters = extract_characters(chapter_text)
    print(f"Personnages détectés : {characters}")

    # Regrouper les alias
    aliases = group_names(characters)
    print(f"Alias regroupés : {aliases}")

    # Créer un dictionnaire de correspondance alias -> nom principal
    alias_to_main = {}
    for group in aliases:
        main_name = group[0]
        for alias in group:
            alias_to_main[alias] = main_name

    # Tokenisation du texte avec stanza
    doc = nlp(chapter_text)
    tokens = [word.text for sentence in doc.sentences for word in sentence.words]

    G = nx.Graph()

    # Ajouter les noeuds avec leurs alias
    for group in aliases:
        main_name = group[0]
        G.add_node(main_name, names=";".join(group))

    # Détecter les co-occurrences dans une fenêtre glissante
    for i in range(len(tokens)):
        for j in range(i + 1, min(i + window_size, len(tokens))):
            token_i = tokens[i]
            token_j = tokens[j]

            # Vérifier si les tokens correspondent à des alias
            if token_i in alias_to_main and token_j in alias_to_main:
                main_i = alias_to_main[token_i]
                main_j = alias_to_main[token_j]

                # Ajouter une arête entre les personnages détectés
                if main_i != main_j:
                    if G.has_edge(main_i, main_j):
                        G[main_i][main_j]['weight'] += 1
                    else:
                        G.add_edge(main_i, main_j, weight=1)

    return G



def process_book(book_folder, book_code, num_chapters):
    """
    Traite un livre en entier pour générer les graphes par chapitre.
    """
    df_dict = {"ID": [], "graphml": []}

    for chapter_num in range(num_chapters):
        chapter_path = os.path.join(book_folder, f"chapter_{chapter_num+1}.txt.preprocessed")
        with open(chapter_path, "r", encoding="utf-8") as file:
            chapter_text = file.read()
        print(f"chapter_{chapter_num+1}.txt.preprocessed")
        G = create_chapter_graph(chapter_text)

        chapter_id = f"{book_code}{chapter_num}"
        graphml = "".join(nx.generate_graphml(G))

        df_dict["ID"].append(chapter_id)
        df_dict["graphml"].append(graphml)

    return pd.DataFrame(df_dict)



    

def main():
    """
    Génère un fichier CSV pour la soumission au leaderboard Kaggle.
    """
    books = [
        ("./paf", "paf", 19),  
        ("./lca", "lca", 18),  
    ]

    all_data = []

    for book_folder, book_code, num_chapters in books:
        book_df = process_book(book_folder, book_code, num_chapters)
        all_data.append(book_df)

    final_df = pd.concat(all_data, ignore_index=True)
    final_df.set_index("ID", inplace=True)
    final_df.to_csv("my_submission.csv")
    print("fini submission")



if __name__ == "__main__":
    main()
