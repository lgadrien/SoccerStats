import os
import pandas as pd

# Chemin où vous souhaitez sauvegarder le fichier
output_dir = 'C:/Users/adri1/Desktop/Epitech 2024-2025/4-SoccerStats/'
output_file = 'cleaned_merged_top5_players_with_squads.csv'

# Vérifier si le répertoire existe, sinon le créer
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Charger le dataset depuis le CSV source
df = pd.read_csv('C:/Users/adri1/Desktop/Epitech 2024-2025/4-SoccerStats/top5-players.csv')

# Inclure la colonne 'Squad' dans les colonnes sélectionnées
columns_to_keep = [
    'Player', 'Nation', 'Age', 'Pos', 'MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG', 'Comp', 'Squad'
]

df_filtered = df[columns_to_keep]

# Mise à jour de l'agrégation pour inclure 'Squad'
agg_dict_with_squad = {
    'Nation': 'first',  # On garde la première valeur pour Nation
    'Age': 'first',     # On garde la première valeur pour Age
    'MP': 'sum',        # On somme le nombre de matchs joués
    'Min': 'sum',       # On somme les minutes jouées
    'Gls': 'sum',       # On somme le nombre de buts marqués
    'Ast': 'sum',       # On somme le nombre d'assists
    'G+A': 'sum',       # On somme le nombre de buts + assists
    'Gls_90': 'mean',   # Moyenne des buts par 90 minutes
    'Ast_90': 'mean',   # Moyenne des assists par 90 minutes
    'xG': 'sum',        # Somme des Expected Goals
    'xAG': 'sum',       # Somme des Expected Assists
    'Comp': ', '.join,  # On garde la liste des compétitions pour chaque joueur
    'Squad': ', '.join  # On garde la liste des équipes (Squads) pour chaque joueur
}

# Grouper les données par joueur, nation, âge, et position tout en appliquant les agrégations spécifiques
df_merged_with_squad = df_filtered.groupby(['Player', 'Nation', 'Age', 'Pos'], as_index=False).agg(agg_dict_with_squad)

# Sauvegarder le fichier dans le répertoire souhaité
df_merged_with_squad.to_csv(os.path.join(output_dir, output_file), index=False)

print(f"Le fichier a été sauvegardé à l'emplacement : {os.path.join(output_dir, output_file)}")
