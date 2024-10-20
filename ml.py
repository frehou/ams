from collections import Counter
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Assurez-vous que les ressources NLTK sont téléchargées
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Initialiser le lemmatiseur et les stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('french'))  # Changer la langue si nécessaire


# Fonction pour générer des n-grammes (séquences de mots)
def generate_ngram_table(text, n=2):
    # Tokenisation du texte en mots, en minuscules pour uniformité
    tokens = re.findall(r'\b\w+\b', text.lower())

    # Normalisation des mots (lemmatisation) et suppression des stop words
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]

    # Génération des n-grammes (séquences de taille n)
    ngrams = list(zip(*[tokens[i:] for i in range(n)]))
    return Counter(ngrams)  # Compte des n-grammes


# Fonction pour afficher les top N co-occurrences
def display_cooccurrence_table(ngram_table, top_n=10):
    print(f"Top {top_n} Co-occurrences :")
    for ngram, count in ngram_table.most_common(top_n):
        print(f"{' '.join(ngram)}: {count} occurrences")


# Lire le texte à partir d'un fichier
file_path = 'C:/Users/DELL/Desktop/fichierTxt/Fondation_et_empire_sample.txt'  # Remplacez par le chemin de votre fichier texte
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

# Générer les bigrammes (co-occurrences de deux mots)
bigram_table = generate_ngram_table(text, n=2)  # Changez 'n' pour d'autres n-grammes (ex: 3 pour trigrammes)

# Afficher les tables de co-occurrences
display_cooccurrence_table(bigram_table, top_n=10)  # Top 10 co-occurrences
