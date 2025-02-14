import streamlit as st
import pandas as pd
from riasec_questions import questions_data  # Assurez-vous d'avoir la variable 'questions_data' définie dans ce fichier

# Initialisation de la session
if 'page' not in st.session_state:
    st.session_state.page = 0
if 'responses' not in st.session_state:
    st.session_state.responses = {cat: [] for cat in questions_data}
if 'result' not in st.session_state:
    st.session_state.result = None

# Chargement du fichier CSV
def load_data():
    try:
        df = pd.read_csv("all_bis.csv", sep=';', on_bad_lines='skip')
        return df
    except Exception as e:
        st.error(f"Erreur de chargement du fichier CSV : {e}")
        return pd.DataFrame()

data = load_data()

# Fonction pour générer une lettre de motivation
def generate_motivation_letter(metier, formation, diplome):
    return f"""Madame, Monsieur,

Je me permets de vous adresser ma candidature pour intégrer la formation {formation}, 
qui correspond parfaitement à mon projet professionnel.

Titulaire d'un {diplome}, je souhaite approfondir mes compétences en {formation} 
afin de m'orienter vers le métier de {metier}.

Dans l’attente de votre retour, je vous prie d’agréer, Madame, Monsieur, mes salutations distinguées.

Signature"""

# Barre latérale
st.sidebar.title("Navigation")
if st.sidebar.button("📋 Passer le test RIASEC"):
    st.session_state.page = 1

review_url = "https://forms.office.com/e/RiBBJkjasa"  
if st.sidebar.button("⭐ Donnez votre avis"):
    st.sidebar.markdown(f"[Cliquez ici pour donner votre avis]({review_url})", unsafe_allow_html=True)

# Page d'accueil
if st.session_state.page == 0:
    st.title("🏠 Accueil")
    st.subheader("Résultat du Test RIASEC")

    riasec_score = st.session_state.result if st.session_state.result else ""
    input_riasec = st.text_input("Entrez votre résultat RIASEC (ex: RIA) ou laissez vide pour utiliser le test", value=riasec_score, max_chars=3).upper()

    if input_riasec and len(input_riasec) != 3:
        st.warning("Veuillez entrer exactement trois lettres correspondant au code RIASEC.")
    else:
        if not data.empty:
            regions = data["Région"].dropna().unique()
            niveau_diplomes = ["Bac", "Bac+1", "Bac+2", "Bac+3", "Bac+4", "Bac+5"]
            aspirations = [
    "Social",
    "Tissez votre avenir avec les métiers de l'industrie textile et de la mode.",
    "Agriculture, sylviculture", "Médical", "BTP", "Industries",
    "Industrie - Chimie", "Élevage, pêche", "Environnement", "Gros Œuvre",
    "Soins animaliers", "Transport", "Service public", "Maintenance",
    "Industrie - Métallurgie", "Gestion administrative", "Architecture",
    "Spectacle", "Industrie - Électronique", "Artisanat d'art",
    "Commerce de gros", "Conseil, orientation et formation",
    "Animation et loisir", "Sport", "Nettoyage", "Commerce de détail",
    "Restauration", "Grande distribution", "Informatique",
    "Culture et patrimoine", "Immobilier", "Tourisme",
    "Étude des sols et des bâtiments", "Comptabilité",
    "Communication et marketing", "Ressources humaines", "Normes",
    "Audiovisuel", "Logistique et courrier", "Sécurité", "Recherche",
    "Hôtellerie", "Industrie - Alimentaire", "Assurance",
    "Télécommunication", "Banque",
    "Découvrez les opportunités de l'édition où les mots inspirent et informent.",
    "Énergie", "Finance", "Enseignement", "Activités juridiques",
    "Imprimerie", "Papier"
]

            col1, col2, col3 = st.columns(3)
            selected_diplome = col1.selectbox("Filtrer par niveau d'étude", ["Tous"] + niveau_diplomes)
            selected_region = col2.selectbox("Filtrer par région", ["Toutes"] + list(regions))
            selected_aspiration = col3.selectbox("Filtrer par aspiration", ["Toutes"] + list(aspirations))

            if selected_diplome != "Tous" and input_riasec:
                filtered_data = data.copy()

                if selected_region != "Toutes":
                    filtered_data = filtered_data[filtered_data["Région"] == selected_region]
                if selected_diplome != "Tous":
                    filtered_data = filtered_data[filtered_data["Niveau attendu"].str.contains(selected_diplome, na=False, case=False)]
                if selected_aspiration != "Toutes":
                    filtered_data = filtered_data[filtered_data["Categorie_y"] == selected_aspiration]

                filtered_data = filtered_data[ 
                    (filtered_data['Lettre RIASEC Principale'].str.strip() == input_riasec[0]) & 
                    (filtered_data['Lettre RIASEC Secondaire'].str.strip() == input_riasec[1]) & 
                    (filtered_data['Lettre RIASEC tertiaire'].str.strip() == input_riasec[2])
                ].head(7)  # Afficher seulement les 7 premiers résultats

                if not filtered_data.empty:
                    st.write("### 🎯 Résultats de la recherche")

                    for index, row in filtered_data.iterrows():
                        with st.container():
                            st.markdown(
                                f"""
                                <div style="
                                    border: 2px solid #f0f0f0;
                                    padding: 15px;
                                    border-radius: 10px;
                                    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                                    margin-bottom: 15px;
                                    background-color: #ffffff;
                                ">
                                    <h4 style="color: #1E88E5;">{row['Metiers']}</h4>
                                    <p><strong>📚 Formation :</strong> {row['Intitulé']}</p>
                                    <p><strong>🏛 Établissement :</strong> {row['Nom']}</p>
                                    <p><strong>📍 Région :</strong> {row['Région']}</p>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            # Génération du bouton avec une mise en page améliorée
                            col1, col2 = st.columns([0.8, 0.2])
                            with col1:
                                if st.button(f"📄 Générer Lettre pour {row['Metiers']}", key=f"btn_{index}"):
                                    st.text_area(
                                        "Lettre de motivation",
                                        generate_motivation_letter(row['Metiers'], row['Intitulé'], selected_diplome),
                                        height=200
                                    )
                            with col2:
                                st.write("")  # Espacement

# Test RIASEC
elif 1 <= st.session_state.page <= len(questions_data):
    pages = list(questions_data.keys())
    current_page = pages[st.session_state.page - 1]
    st.title(f"📋 {current_page}")
    st.progress(st.session_state.page / len(questions_data))

    # Récupération des réponses précédentes pour chaque catégorie
    responses = st.session_state.responses[current_page]

    # Afficher les questions pour chaque catégorie
    for category, questions in questions_data[current_page].items():
        st.subheader(category)
        for question in questions:
            if isinstance(question, dict):
                options = ["0", "0.5", "1"]
                response = st.radio(question["question"], options, key=f"{category}_{question['question']}")
                responses.append(float(response))
            else:
                checked = st.checkbox(question, key=f"{category}_{question}")
                if checked:
                    responses.append(1)

    # Navigation entre les pages
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.page > 1:
            st.button("⬅️ Précédent", on_click=lambda: setattr(st.session_state, 'page', st.session_state.page - 1))
    with col2:
        if st.session_state.page < len(questions_data):
            st.button("➡️ Suivant", on_click=lambda: setattr(st.session_state, 'page', st.session_state.page + 1))
        else:
            if st.button("🎯 Voir les résultats"):
                # Calculer les résultats du test
                scores = {cat: sum(st.session_state.responses[cat]) for cat in questions_data}
                sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                top_three = ''.join([cat[0] for cat, _ in sorted_categories[:3]])
                st.session_state.result = top_three
                st.session_state.page = 0