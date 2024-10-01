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
def ensure_numeric(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

# Vérifier que les colonnes nécessaires sont bien numériques et gérer les valeurs manquantes
numeric_columns = ['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']
df = ensure_numeric(df, numeric_columns)

# Fonction pour créer un radar chart interactif avec Plotly pour un joueur
def radar_chart_individual_plotly(player_stats, player_name):
    categories = ['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']
    values = player_stats[categories].values.flatten().tolist()

    # Normaliser les valeurs entre 0 et 1
    scaler = MinMaxScaler()
    values_normalized = scaler.fit_transform(np.array(values).reshape(-1, 1)).flatten().tolist()

    # Créer le radar chart pour un joueur
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_normalized,
        theta=categories,
        fill='toself',
        name=player_name,
        marker=dict(color='blue'),
        opacity=0.7
    ))

    # Ajuster la mise en page
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=False,
        title=f"Radar Chart - {player_name}"
    )

    # Afficher le radar chart dans Streamlit
    st.plotly_chart(fig)

# Fonction pour créer un radar chart comparatif interactif avec Plotly
def radar_chart_comparative_plotly(player_1_stats, player_2_stats, player_1_name, player_2_name):
    categories = ['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']
    
    # Extraire les valeurs des statistiques pour les deux joueurs
    values_1 = player_1_stats[categories].values.flatten().tolist()
    values_2 = player_2_stats[categories].values.flatten().tolist()

    # Normaliser les valeurs entre 0 et 1 pour les deux joueurs
    scaler = MinMaxScaler()
    combined_values = np.array([values_1, values_2])
    combined_normalized = scaler.fit_transform(combined_values)

    # Tracer le radar chart avec Plotly
    fig = go.Figure()

    # Ajouter le premier joueur
    fig.add_trace(go.Scatterpolar(
        r=combined_normalized[0], 
        theta=categories, 
        fill='toself', 
        name=player_1_name,
        marker=dict(color='blue'),
        opacity=0.7
    ))

    # Ajouter le second joueur
    fig.add_trace(go.Scatterpolar(
        r=combined_normalized[1], 
        theta=categories, 
        fill='toself', 
        name=player_2_name,
        marker=dict(color='red'),
        opacity=0.7
    ))

    # Ajuster la mise en page
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1])
        ),
        showlegend=True,
        title=f"Radar Chart Comparatif - {player_1_name} vs {player_2_name}"
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

# Explication des en-têtes des tableaux
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
st.sidebar.title("Filtres")

# Recherche de joueur par nom
player_name = st.sidebar.text_input("Chercher un joueur")

# Sélectionner un club
selected_club = st.sidebar.selectbox(
    'Sélectionner un club',
    options=['Tous les clubs'] + list(df['Squad'].unique())
)

# Sélectionner un championnat
selected_comp = st.sidebar.selectbox(
    'Sélectionner un championnat',
    options=['Toutes les compétitions'] + list(df['Comp'].unique())
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
    options=['Tous les postes'] + list(positions.keys())
)

# Filtrer par âge
age_min, age_max = st.sidebar.slider(
    'Filtrer par âge',
    int(df['Age'].min()), int(df['Age'].max()), 
    (int(df['Age'].min()), int(df['Age'].max()))
)

# Filtrer par nombre de matchs joués (MP)
mp_min, mp_max = st.sidebar.slider(
    'Filtrer par matchs joués',
    int(df['MP'].min()), int(df['MP'].max()), 
    (int(df['MP'].min()), int(df['MP'].max()))
)

# Filtrer par nombre de buts (Gls)
gls_min, gls_max = st.sidebar.slider(
    'Filtrer par nombre de buts (Gls)',
    int(df['Gls'].min()), int(df['Gls'].max()), 
    (int(df['Gls'].min()), int(df['Gls'].max()))
)

# Filtrer par nombre d'assists (Ast)
ast_min, ast_max = st.sidebar.slider(
    'Filtrer par nombre d\'assists (Ast)',
    int(df['Ast'].min()), int(df['Ast'].max()), 
    (int(df['Ast'].min()), int(df['Ast'].max()))
)

# Appliquer les filtres au dataset
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
st.title("Résultats filtrés")
st.dataframe(filtered_df.reset_index(drop=True))

# Comparaison de deux joueurs
st.title("Comparaison de deux joueurs :")

# Sélectionner deux joueurs pour la comparaison
player_1 = st.selectbox("Sélectionner le premier joueur", df['Player'].unique())
player_2 = st.selectbox("Sélectionner le second joueur", df['Player'].unique())

# Extraire les statistiques des deux joueurs
player_1_stats = df[df['Player'] == player_1][['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']]
player_2_stats = df[df['Player'] == player_2][['MP', 'Min', 'Gls', 'Ast', 'G+A', 'Gls_90', 'Ast_90', 'xG', 'xAG']]

# Afficher la comparaison des statistiques avec l'équipe
st.subheader(f"Comparaison entre {player_1} et {player_2}")

# Afficher les radars individuels des joueurs
col1, col2 = st.columns(2)

# Afficher le radar chart du premier joueur
with col1:
    st.write(f"Statistiques de {player_1}")
    radar_chart_individual_plotly(player_1_stats, player_1)

# Afficher le radar chart du second joueur
with col2:
    st.write(f"Statistiques de {player_2}")
    radar_chart_individual_plotly(player_2_stats, player_2)

# Afficher le radar chart comparatif des deux joueurs
st.subheader("Radar Chart Comparatif")
radar_chart_comparative_plotly(player_1_stats, player_2_stats, player_1, player_2)

# === Idée 2 : Top Performers ===
st.subheader("Top Performers")

# Sélectionner le critère pour afficher les meilleurs joueurs (buts, assists, etc.)
selected_stat = st.selectbox("Sélectionner une statistique pour classer les joueurs", ['Gls', 'Ast', 'G+A', 'xG', 'xAG'])

# Afficher les 10 meilleurs joueurs selon le critère sélectionné
top_performers = df.sort_values(by=selected_stat, ascending=False).head(10)
st.write(f"Top 10 joueurs selon {selected_stat}")
st.dataframe(top_performers[['Player', 'Squad', selected_stat, 'Min', 'MP']])

# === Idée 7 : Heatmap des positions des joueurs ===
# === Amélioration de la Heatmap des positions des joueurs ===
st.subheader("Heatmap des positions des joueurs")

# Sélectionner les équipes ou les joueurs à inclure dans la heatmap
selected_squads = st.multiselect("Sélectionner des équipes pour afficher la heatmap", df['Squad'].unique())

if len(selected_squads) > 0:
    # Filtrer les données pour les équipes sélectionnées
    heatmap_data = df[df['Squad'].isin(selected_squads)]
    
    # Créer une pivot table pour générer les valeurs de la heatmap (ex: nombre de buts par poste et équipe)
    heatmap_matrix = heatmap_data.pivot_table(index='Pos', columns='Squad', values='Gls', aggfunc='sum', fill_value=0)
    
    # Convertir explicitement les index et colonnes en listes
    x_labels = heatmap_matrix.columns.tolist()
    y_labels = heatmap_matrix.index.tolist()
    z_values = heatmap_matrix.values
    
    # Créer la heatmap avec Plotly, ajout des annotations et des ajustements de couleurs
    fig = ff.create_annotated_heatmap(
        z=z_values,
        x=x_labels,
        y=y_labels,
        colorscale='Blues',  # Utilisation d'une palette de couleurs "Blues" pour une meilleure lisibilité
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
    
    # Ajuster le style des annotations
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 12  # Taille du texte des annotations
        fig.layout.annotations[i].font.color = 'black'  # Couleur des annotations pour une meilleure lisibilité
    
    st.plotly_chart(fig)

# Footer pour rendre la page plus agréable
st.markdown("***")
st.write("Tableau de bord créé pour analyser les performances des joueurs dans les 5 premières ligues mondiales (saison 2023/2024).")
