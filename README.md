# Extraction de Réseaux de Personnages

Ce projet permet d'extraire des réseaux de personnages à partir de chapitres de livres et de générer un fichier CSV pour soumission au leaderboard Kaggle.

## Prérequis

- **Python 3.8 ou supérieur** installé.
- Les bibliothèques Python suivantes :
  - `stanza`
  - `networkx`
  - `pandas`
  - `flair`
  - `re`
  - `os`

Pour installer les dépendances, exécutez la commande suivante :

```bash
pip install stanza networkx pandas flair
Assurez-vous également d'avoir téléchargé le modèle linguistique fr pour Stanza et le modèle flair/ner-english-large pour Flair. Ces modèles sont automatiquement téléchargés lors de la première exécution si non présents.

Structure des fichiers
extraction.py : Fichier principal contenant le code pour extraire les réseaux de personnages.
antidic.txt : Fichier contenant l'antidictionnaire utilisé pour filtrer les mots indésirables.
lca et paf : Dossiers contenant les chapitres prétraités des livres.

Les fichiers des chapitres doivent être nommés sous la forme chapter_X.txt.preprocessed, où X correspond au numéro du chapitre.

## Instructions
Placez le fichier antidic.txt dans le même dossier que extraction.py.
Assurez-vous que les dossiers lca et paf contiennent les fichiers des chapitres prétraités.
Exécutez le programme avec la commande suivante :

python extraction.py

## Résultat
Le programme génère un fichier my_submission.csv dans le répertoire actuel. Ce fichier contient les graphes de personnages pour les livres spécifiés.

## Exemple de sortie
Une fois le script exécuté, vous verrez des logs indiquant les étapes du traitement, comme l'extraction des personnages et la génération des graphes.

Le fichier my_submission.csv est prêt pour être soumis au leaderboard Kaggle.
