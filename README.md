README: Extraction de Réseaux de Personnages

Présentation

Ce programme permet d'extraire des réseaux de personnages à partir des chapitres d'un livre, en vue de soumettre un fichier CSV au leaderboard Kaggle. Les réseaux sont construits à l'aide de co-occurrences des noms de personnages dans le texte.

Prérequis

Python 3.7 ou supérieur

Bibliothèques Python suivantes :

stanza

networkx

pandas

os

re

flair

Pour installer les dépendances, exécutez :

pip install stanza networkx pandas flair

Fichiers requis

antidic.txt :

Un fichier contenant un antidictionnaire (mots à exclure) doit être présent dans le même dossier que le fichier Python extraction.py.

Dossiers de chapitres :

Deux dossiers, lca et paf, contenant les fichiers prétraités des chapitres :

Les fichiers doivent avoir le format chapter_X.txt.preprocessed (où X est le numéro du chapitre).

Instructions pour l'exécution

Assurez-vous que les fichiers suivants sont présents dans le répertoire de travail :

extraction.py

antidic.txt

Dossiers lca et paf avec leurs chapitres respectifs.

Lancez le script Python extraction.py :

python extraction.py

Une fois l'exécution terminée, un fichier my_submission.csv sera généré dans le répertoire de travail. Ce fichier contient les graphes de personnages, prêts à être soumis au leaderboard Kaggle.

Structure du fichier CSV

Le fichier CSV généré aura les colonnes suivantes :

ID : Identifiant unique pour chaque chapitre.

graphml : Représentation du graphe des personnages au format GraphML.

Notes supplémentaires

Les graphes sont construits en utilisant les co-occurrences des noms de personnages dans une fenêtre glissante de 25 mots.

Les alias de personnages sont regroupés pour garantir la précision des connexions dans les graphes.

Assurez-vous que les chapitres sont prétraités et placés correctement dans les dossiers lca et paf avant de lancer le programme.
