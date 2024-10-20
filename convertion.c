#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define TAILLE_MAX 100000000

void PdfToText(char* nom_dossier) {
    char *ch;
    ch = (char *) malloc(TAILLE_MAX * sizeof(char));
    
    char *line;
    line = (char *) malloc(TAILLE_MAX * sizeof(char));
    
    // Lister les fichiers .pdf dans le dossier sous Windows
    snprintf(ch, TAILLE_MAX, "dir /b \"%s\\*.pdf\" > tst.txt", nom_dossier);
    system(ch); // Mettre les noms des fichiers .pdf dans un fichier "tst.txt"
    
    // Ouvrir le fichier "tst.txt"
    FILE* fichier = fopen("tst.txt", "r");
    if (fichier == NULL) {
        perror("Erreur d'ouverture du fichier tst.txt");
        free(ch);
        free(line);
        return;
    }
    
    // Parcourir le fichier "tst.txt"
    while (fgets(line, TAILLE_MAX, fichier) != NULL) {
        // Retirer le '\n' de la ligne lue
        line[strcspn(line, "\n")] = 0;
        
        // Retirer l'extension .pdf
        char *dot = strrchr(line, '.');
        if (dot != NULL) {
            *dot = '\0'; // Supprimer l'extension en plaçant un caractère nul à la position du '.'
        }
        
        // Construire la commande pdftotext pour enregistrer le fichier texte sans l'extension .pdf
        snprintf(ch, TAILLE_MAX, "pdftotext \"%s\\%s.pdf\" \"%s\\%s.txt\"", nom_dossier, line, nom_dossier, line);
        system(ch);
    }
    
    fclose(fichier);
    
    // Supprimer le fichier temporaire "tst.txt"
    system("del tst.txt");
    
    free(ch);
    free(line);
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <nom_dossier>\n", argv[0]);
        return EXIT_FAILURE;
    }

    PdfToText(argv[1]);

    printf("Conversion terminée. Les fichiers .txt sont dans le dossier '%s'.\n", argv[1]);
    
    return EXIT_SUCCESS;
}
