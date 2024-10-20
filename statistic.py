import re


def generate_corpus_statistics(text):
    nb_characters = len(text)

    nb_words = len(re.findall(r'\b\w+\b', text))

    nb_sentences = len(re.findall(r'[.!?]', text))

    return nb_characters, nb_words, nb_sentences


def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text


file_path = 'C:/Users/DELL/Desktop/fichierTxt/Seconde_Fondation_sample.txt'  # Remplacez par votre chemin de fichier hamza

text = read_text_from_file(file_path)

nb_characters, nb_words, nb_sentences = generate_corpus_statistics(text)

print(f"Nombre de caractères : {nb_characters}")
print(f"Nombre de mots : {nb_words}")
print(f"Nombre de phrases : {nb_sentences}")
