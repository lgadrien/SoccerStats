import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
import plotly.figure_factory as ff

# Charger le dataset nettoyé
df = pd.read_csv('DataSet_Cleaned.csv')

# Fonction pour s'assurer que les colonnes sont bien numériques et gérer les valeurs manquantes
# Cette fonction convertit les colonnes spécifiées en valeurs numériques et remplace les valeurs manquantes par 0
def ensure_numeric(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

# Vérifier que les colonnes nécessaires sont bien numériques et gérer les valeurs manquantes
# Liste des colonnes à convertir en numérique
numeric_columns = ['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']
df = ensure_numeric(df, numeric_columns)

# Fonction pour créer un radar chart interactif avec Plotly pour un joueur
# Cette fonction génère un graphique radar basé sur les statistiques d'un joueur donné
def radar_chart_individual_plotly(player_stats, player_name):
    # Définition des catégories à afficher sur le radar chart
    categories = ['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']
    values = player_stats[categories].values.flatten().tolist()  # Extraire les valeurs des stats

    # Normaliser les valeurs entre 0 et 1 pour garantir une échelle cohérente
    scaler = MinMaxScaler()
    values_normalized = scaler.fit_transform(np.array(values).reshape(-1, 1)).flatten().tolist()

    # Création du radar chart avec Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_normalized,
        theta=categories,
        fill='toself',
        name=player_name,
        marker=dict(color='blue'),
        opacity=0.7
    ))

    # Ajuster la mise en page du graphique
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False,
        title=f"Radar Chart - {player_name}"
    )

    # Affichage du graphique radar dans Streamlit
    st.plotly_chart(fig)

# Explication des en-têtes des tableaux
# Affiche une explication textuelle des colonnes principales du dataset
st.title("Explication des en-têtes des tableaux")
st.write("""
Voici une description des principales colonnes utilisées dans les tableaux et graphiques :

- **MP** : Nombre total de matchs joués par le joueur.
- **Min** : Minutes jouées par le joueur au total.
- **Gls** : Nombre de buts marqués par le joueur.
- **Ast** : Nombre de passes décisives réalisées par le joueur.
- **G+A** : Combinaison des buts et des passes décisives pour évaluer les performances offensives globales.
- **Gls_90** : Nombre moyen de buts par 90 minutes jouées.
- **Ast_90** : Nombre moyen de passes décisives par 90 minutes jouées.
- **xG** : Expected Goals (buts attendus), représentant la qualité des occasions créées par le joueur.
- **xAG** : Expected Assists (passes décisives attendues), représentant la qualité des passes conduisant potentiellement à des buts.
""")

# Sidebar rétractable pour les filtres
# Interface de filtrage des données par différents critères dans la barre latérale
st.sidebar.title("Filtres")

# Recherche de joueur par nom
player_name = st.sidebar.text_input("Chercher un joueur")

# Sélectionner un club
selected_club = st.sidebar.selectbox(
    'Sélectionner un club',
    options=['Tous les clubs'] + list(df['Squad'].unique())  # Liste des clubs disponibles
)

# Sélectionner un championnat
selected_comp = st.sidebar.selectbox(
    'Sélectionner un championnat',
    options=['Toutes les compétitions'] + list(df['Comp'].unique())  # Liste des compétitions
)

# Sélectionner un poste
positions = {
    'Gardien de but (GK)': 'GK',
    'Défenseur (DF)': 'DF',
    'Milieu de terrain (MF)': 'MF',
    'Attaquant (FW)': 'FW'
}

selected_pos = st.sidebar.selectbox(
    'Sélectionner un poste',
    options=['Tous les postes'] + list(positions.keys())  # Liste des positions possibles
)

# Filtrer par âge
age_min, age_max = st.sidebar.slider(
    'Filtrer par âge',
    int(df['Age'].min()), int(df['Age'].max()), 
    (int(df['Age'].min()), int(df['Age'].max()))  # Plage d'âge minimum et maximum
)

# Filtrer par nombre de matchs joués (MP)
mp_min, mp_max = st.sidebar.slider(
    'Filtrer par matchs joués',
    int(df['MP'].min()), int(df['MP'].max()), 
    (int(df['MP'].min()), int(df['MP'].max()))  # Plage du nombre de matchs
)

# Filtrer par nombre de buts (Gls)
gls_min, gls_max = st.sidebar.slider(
    'Filtrer par nombre de buts (Gls)',
    int(df['Gls'].min()), int(df['Gls'].max()), 
    (int(df['Gls'].min()), int(df['Gls'].max()))  # Filtrage des buts marqués
)

# Filtrer par nombre d'assists (Ast)
ast_min, ast_max = st.sidebar.slider(
    'Filtrer par nombre d\'assists (Ast)',
    int(df['Ast'].min()), int(df['Ast'].max()), 
    (int(df['Ast'].min()), int(df['Ast'].max()))  # Filtrage des passes décisives
)

# Appliquer les filtres au dataset
# Les filtres sont appliqués en fonction des critères sélectionnés
filtered_df = df[
    (df['Player'].str.contains(player_name, case=False)) &
    ((df['Squad'] == selected_club) if selected_club != 'Tous les clubs' else True) &
    ((df['Comp'] == selected_comp) if selected_comp != 'Toutes les compétitions' else True) &
    ((df['Pos'].str.contains(positions[selected_pos])) if selected_pos != 'Tous les postes' else True) &
    (df['Age'] >= age_min) & (df['Age'] <= age_max) &
    (df['MP'] >= mp_min) & (df['MP'] <= mp_max) &
    (df['Gls'] >= gls_min) & (df['Gls'] <= gls_max) &
    (df['Ast'] >= ast_min) & (df['Ast'] <= ast_max)
]

# Afficher les résultats filtrés
# Affiche un tableau interactif des données filtrées
st.title("Résultats filtrés")
st.dataframe(filtered_df.reset_index(drop=True))

# Dictionnaire pour rendre les statistiques plus claires dans le tableau et les filtres
stat_translation = {
    'Gls': 'Buts marqués',
    'Ast': 'Passes décisives',
    'G+A': 'Buts + Passes',
    'xG': 'Buts attendus (xG)',
    'xAG': 'Passes décisives attendues (xAG)'
}

# Fonction pour comparer les statistiques de deux joueurs et déterminer lequel est meilleur
def compare_players(player_1_stats, player_2_stats, player_1_name, player_2_name):
    # Catégories à comparer avec des noms complets
    categories = {
        'MP': 'Matches joués',
        'Min': 'Minutes jouées',
        'Gls': 'Buts marqués',
        'Ast': 'Passes décisives',
        'G+A': 'Buts + Passes',
        'Gls_90': 'Buts par 90 minutes',
        'Ast_90': 'Passes décisives par 90 minutes',
        'xG': 'Buts attendus (xG)',
        'xAG': 'Passes attendues (xAG)'
    }
    
    total_categories = len(categories)
    
    # Extraire les valeurs des statistiques des deux joueurs
    values_1 = player_1_stats[list(categories.keys())].values.flatten().tolist()
    values_2 = player_2_stats[list(categories.keys())].values.flatten().tolist()

    # Initialiser les scores des deux joueurs
    player_1_score = 0
    player_2_score = 0

    # Liste pour stocker les détails de la comparaison
    comparison_details = []
    
    # Comparer chaque statistique
    for i, category in enumerate(categories):
        stat_player_1 = values_1[i]
        stat_player_2 = values_2[i]
        
        if stat_player_1 > stat_player_2:
            player_1_score += 1  # Joueur 1 est meilleur pour cette statistique
            comparison_details.append(f"{categories[category]}: {player_1_name} est meilleur")
        elif stat_player_2 > stat_player_1:
            player_2_score += 1  # Joueur 2 est meilleur pour cette statistique
            comparison_details.append(f"{categories[category]}: {player_2_name} est meilleur")
        else:
            comparison_details.append(f"{categories[category]}: Égalité")

    # Calcul du score final en pourcentage pour chaque joueur
    player_1_final_score = (player_1_score / total_categories) * 100
    player_2_final_score = (player_2_score / total_categories) * 100

    # Résultat final basé sur les scores
    if player_1_final_score > player_2_final_score:
        result_message = f"{player_1_name} est globalement meilleur que {player_2_name}"
    elif player_2_final_score > player_1_final_score:
        result_message = f"{player_2_name} est globalement meilleur que {player_1_name}"
    else:
        result_message = f"{player_1_name} et {player_2_name} sont égaux sur leurs performances globales"

    return player_1_final_score, player_2_final_score, comparison_details, result_message

# Comparaison de deux joueurs
st.title("Comparateur de joueurs :")

# Sélectionner deux joueurs pour la comparaison avec des clés uniques
player_1 = st.selectbox("Sélectionner le premier joueur", df['Player'].unique(), key="player_1_selector")
player_2 = st.selectbox("Sélectionner le second joueur", df['Player'].unique(), key="player_2_selector")

# Extraire les statistiques des deux joueurs
player_1_stats = df[df['Player'] == player_1][['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']]
player_2_stats = df[df['Player'] == player_2][['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']]

# Comparer les deux joueurs et obtenir les résultats
player_1_score, player_2_score, comparison_details, result_message = compare_players(player_1_stats, player_2_stats, player_1, player_2)

# Afficher les détails de la comparaison
st.subheader(f"Comparaison des statistiques : {player_1} vs {player_2}")
for detail in comparison_details:
    st.write(detail)

# Afficher le résultat final de la comparaison
st.subheader("Conclusion :")
st.write(result_message)

# Afficher les scores de chaque joueur en pourcentage
st.write(f"Score de {player_1} : {player_1_score:.2f}/100")
st.write(f"Score de {player_2} : {player_2_score:.2f}/100")

# === Idée 2 : Top Performers (Améliorée avec noms clairs pour les statistiques) ===
# Classement des meilleurs joueurs selon une statistique spécifique choisie par l'utilisateur
st.subheader("Top Performers")

# Sélectionner le critère pour afficher les meilleurs joueurs (buts, passes, etc.)
selected_stat_display = st.selectbox("Sélectionner une statistique pour classer les joueurs", list(stat_translation.values()))

# Récupérer la clé associée au terme sélectionné dans le dictionnaire
selected_stat = {v: k for k, v in stat_translation.items()}[selected_stat_display]

# Afficher les 10 meilleurs joueurs selon le critère sélectionné
top_performers = df.sort_values(by=selected_stat, ascending=False).head(10)
st.write(f"Top 10 joueurs selon {selected_stat_display}")
st.dataframe(top_performers[['Player', 'Squad', selected_stat, 'Min', 'MP']].rename(columns=stat_translation))


# Dictionnaire pour mapper les abréviations des positions en français
position_translation = {
    'GK': 'Gardien de but',
    'DF': 'Défenseur',
    'MF': 'Milieu de terrain',
    'FW': 'Attaquant'
}

# Remplacer les abréviations des positions par les termes complets en français
df['Pos'] = df['Pos'].map(position_translation)

# Définir l'ordre spécifique des postes : Gardien de but, Défenseur, Milieu de terrain, Attaquant
ordered_positions = ['Gardien de but', 'Défenseur', 'Milieu de terrain', 'Attaquant']

# === Heatmap des positions des joueurs (Améliorée avec couleurs chaudes et ordre des postes) ===
# Heatmap affichant le nombre de buts par position et par équipe
st.subheader("Heatmap des positions qui marquent des buts")

# Sélectionner les équipes ou les joueurs à inclure dans la heatmap
selected_squads = st.multiselect("Sélectionner des équipes pour afficher la heatmap", df['Squad'].unique())

if len(selected_squads) > 0:
    # Filtrer les données pour les équipes sélectionnées
    heatmap_data = df[df['Squad'].isin(selected_squads)]
    
    # Créer une pivot table pour générer les valeurs de la heatmap (ex: nombre de buts par poste et équipe)
    heatmap_matrix = heatmap_data.pivot_table(index='Pos', columns='Squad', values='Gls', aggfunc='sum', fill_value=0)
    
    # Réorganiser l'index pour que les positions suivent l'ordre spécifique
    heatmap_matrix = heatmap_matrix.reindex(ordered_positions)
    
    # Convertir explicitement les index et colonnes en listes
    x_labels = heatmap_matrix.columns.tolist()
    y_labels = heatmap_matrix.index.tolist()
    z_values = heatmap_matrix.values
    
    # Créer la heatmap avec Plotly, ajout des annotations et des ajustements de couleurs
    fig = ff.create_annotated_heatmap(
        z=z_values,
        x=x_labels,
        y=y_labels,
        colorscale='Reds',  # Utilisation d'une palette de couleurs "Reds" pour une meilleure lisibilité
        showscale=True,
        annotation_text=np.round(z_values, decimals=1),  # Affichage des valeurs sur chaque cellule
        hoverinfo="z"  # Afficher les valeurs au survol des cellules
    )
    
    # Ajuster la mise en page et redimensionner automatiquement selon le nombre d'équipes
    fig.update_layout(
        title="Nombre de buts marqués par position et par équipe",
        xaxis=dict(title='Équipes'),
        yaxis=dict(title='Positions'),
        autosize=False,
        width=600 + len(x_labels) * 40,  # Ajuste la largeur en fonction du nombre d'équipes
        height=400 + len(y_labels) * 40  # Ajuste la hauteur en fonction du nombre de positions
    )
    
    # Ajuster le style des annotations pour les rendre plus visibles
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 12  # Taille du texte des annotations
        fig.layout.annotations[i].font.color = 'black'  # Couleur des annotations pour une meilleure lisibilité
    
    # Afficher la heatmap dans Streamlit
    st.plotly_chart(fig)

# Footer pour rendre la page plus agréable
# Ajoute un footer avec un message informatif
st.markdown("***")
st.write("Tableau de bord créé pour analyser les performances des joueurs dans les 5 premières ligues mondiales (saison 2023/2024).")
