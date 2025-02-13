import dash
from dash import html, dcc, Output, Input, dash_table, ALL, State
from flask import send_file
import flask
import fonctions
import pandas as pd
import os
from flask import Flask, request, jsonify
server = flask.Flask(__name__)
app = dash.Dash(__name__,  server=server, suppress_callback_exceptions=True)

@server.route('/get_riasec', methods=['POST'])
def get_riasec():
    data = request.get_json()
    top_three = data.get("riasec", "")
    
    print("Top 3 RIASEC reçu :", top_three)  
    
    return top_three


data = pd.read_csv('all_bis.csv')
aspirations_liste = data["Categorie_y"].unique()
aspirations = [{'label':x, 'value':x} for x in aspirations_liste if len(x) < 25]
riasec_options = [
    {"label": "R - Réaliste", "value": "R"},
    {"label": "I - Investigateur", "value": "I"},
    {"label": "A - Artistique", "value": "A"},
    {"label": "S - Social", "value": "S"},
    {"label": "E - Entreprenant", "value": "E"},
    {"label": "C - Conventionnel", "value": "C"},
]

regions_liste = data["région"].unique()
regions = [{'label':x, 'value':x} for x in regions_liste]
departements = [{"label":f"{x:02d}", "value":x} for x in range(1,96)]
departements.append({"label":"971", "value": 971})
departements.append({"label":"972", "value": 972})
departements.append({"label":"973", "value": 973})
departements.append({"label":"974", "value": 974})
departements.append({"label":"976", "value": 976})

niveaux_diplomes = [{"label": "Bac", "value": "bac"},
    {"label": "Bac +1", "value": "bac_1"},
    {"label": "Bac +2", "value": "bac_2"},
    {"label": "Bac +3", "value": "bac_3"},
    {"label": "Bac +4", "value": "bac_4"},
    {"label": "Bac +5", "value": "bac_5"},
]



composants = html.Div(
    children=[
        html.Div(
            children=[
                # 📌 Dropdown Diplôme
                dcc.Dropdown(
                    id="dropdown-diplome",
                    options=niveaux_diplomes,
                    placeholder="Indiquez le niveau du dernier diplôme obtenu",
                    style={"width": "250px", "height": "40px"}  # ✅ Même hauteur que l'input
                ),

                # 📌 Bloc contenant l'input et le message d'erreur (Aligné avec les autres)
                html.Div(
                    children=[
                        dcc.Input(
                            id="riasec-score",
                            type="text",
                            placeholder="Entrez votre résultat RIASEC",
                            maxLength=6,
                            style={"width": "250px", "height": "40px", "borderRadius": "5px"}  # ✅ Même hauteur que les dropdowns
                        ),
                        html.Div(
                            id="score-feedback",

                            style={
                                "color": "red", 
                                "fontSize": "12px", 
                                "marginTop": "3px",
                                "minHeight": "16px",  # ✅ Réserve un espace fixe pour éviter le déplacement
                                "visibility": "hidden"  # ✅ Caché au départ mais espace maintenu
                            }
                        )
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "center",  # ✅ Aligné avec les dropdowns
                        "justifyContent": "center",
                        "width": "250px"  # ✅ Même largeur que les autres inputs
                    }
                ),

                # 📌 Dropdown Département
                dcc.Dropdown(
                    id="dropdown-departement",
                    options=regions,
                    placeholder="Filtrez par un département",
                    style={"width": "250px", "height": "40px"}  # ✅ Même hauteur que les autres
                ),
                dcc.Dropdown(
                    id="dropdown-aspirations",
                    options=aspirations,
                    placeholder="Choisissez une aspiration",
                    style={"width": "250px", "height": "40px"}  # ✅ Même hauteur que les autres
                ),

                # 📌 Bouton pour le questionnaire
                html.A(
                    html.Button("Ouvrir le questionnaire RIASEC", style={"height": "40px"}),  # ✅ Même hauteur que les autres
                    href="/assets/test_riasec.html",
                    target="_blank"
                ), dcc.Download(id="download-motivation-letter")
            ],
            style={
                "display": "flex",
                "flexDirection": "row",
                "gap": "20px",
                "justifyContent": "center",
                "alignItems": "center",  # ✅ Aligné parfaitement sur la ligne
                "marginTop": "20px"
            }
        )
    ]
)





app.layout = html.Div([html.Div(
    children=[
        html.Div(
            html.Img(
                src="https://sharetribe-assets.imgix.net/66599475-18f2-455e-b2a0-dada516c5c3e/raw/f1/1b4273dea865e28fe4d2c3de1ba0bca7e0ae2d?auto=format&fit=clip&h=72&w=640&s=4f630339c7c28b668698c63be79c474d",
                style={"display": "block", "margin": "auto", "maxWidth": "100%", "height": "auto"}
            ),
            style={"textAlign": "center", "paddingTop": "20px"} 
        ),
        html.Div(
            html.H3(
                "Découvrez les meilleures formations selon votre profil !",
                style={"textAlign": "center", "fontWeight": "normal", "marginTop": "10px"}
            )
        ),
    ],
    style={"display": "flex", "flexDirection": "column", "alignItems": "center"}  
),composants,
html.Br(),
html.Div(id="results", style={'display': "none"})
]
)

PDF_FOLDER = "generated_pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

def generate_motivation_letter(metier, formation, diplome, filename):
    file_path = os.path.join(PDF_FOLDER, filename)
    with open(file_path, "w") as f:
        f.write(f"""Madame, Monsieur,

Je me permets de vous adresser ma candidature pour intégrer la formation {formation}, 
qui correspond parfaitement à mon projet professionnel.

Titulaire d'un {diplome}, je souhaite approfondir mes compétences en {formation} 
afin de m'orienter vers le métier de {metier}.

Dans l’attente de votre retour, je vous prie d’agréer, Madame, Monsieur, mes salutations distinguées.

Signature""")
    return file_path

def display_results():
    data = [
        {"Nom du métier": "Data Scientist", "Nom de la formation": "Master IA", "Diplome": "Bac+5"},
        {"Nom du métier": "Ingénieur Machine Learning", "Nom de la formation": "MSc Data Science", "Diplome": "Bac+5"},
        {"Nom du métier": "Analyste en Big Data", "Nom de la formation": "Licence Informatique", "Diplome": "Bac+3"},
    ]

    df = pd.DataFrame(data)

    return dash_table.DataTable(
        id="results-table",
        columns=[
            {"name": "Nom du métier", "id": "Nom du métier"},
            {"name": "Nom de la formation", "id": "Nom de la formation"},
            {"name": "Lettre de motivation", "id": "Lettre de motivation"}
        ],
        data=df.to_dict("records"),
        style_cell={"textAlign": "left", "padding": "10px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#f4f4f4"},
        style_table={"width": "80%", "margin": "auto"},
        style_data_conditional=[
            {
                "if": {"column_id": "Lettre de motivation"},
                "width": "150px",
                "textAlign": "center"
            }
        ]
    )

def create_table(filtered_df):
    
    filtered_df = filtered_df[['Metiers', 'Intitulé', 'nom']].drop_duplicates(subset=['Metiers', 'Intitulé']).head(7)

    


    # Retourner un dash_table.DataTable
    return dash_table.DataTable(
        columns=[{"name": col, "id": col} for col in ['Metiers','Intitulé', 'nom']],
        data=filtered_df.to_dict("records"),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'fontWeight': 'bold', 'backgroundColor': '#f4f4f4'},
        page_size=7,  
    )
@app.callback(
    Output("results", "children"),  
    Output("results", "style"),
    Input("dropdown-diplome", "value"),
    Input("riasec-score", "value"),
    Input("dropdown-departement", "value"),
    Input("dropdown-aspirations", "value")
)
def update_table(diplome, riasec, region, aspiration):
    if not diplome or not riasec or len(riasec) != 3:
        return "", {"display": "none"}
    df =pd.read_csv('all_bis.csv')
    letters = riasec
    df['Lettre RIASEC Principale'] = df['Lettre RIASEC Principale'].str.strip()
    df['Lettre RIASEC Secondaire'] = df['Lettre RIASEC Secondaire'].str.strip()
    df['Lettre RIASEC tertiaire'] = df['Lettre RIASEC tertiaire'].str.strip()
    df['Niveau attendu'] = df['Niveau attendu'].str.strip().str.lower().str.replace(" ", "")
    df['CP'] = df['CP'].astype(str).str.strip().str[:2]

    
    filtered_df = df[df['Lettre RIASEC Principale'] == letters[0]] 
    filtered_df = filtered_df[filtered_df['Lettre RIASEC Secondaire'] == letters[1]]
    
    new_df = filtered_df[filtered_df['Lettre RIASEC tertiaire'] == letters[2]]  # Filtrage 3
    if not new_df.empty:
        print("helllo")
        filtered_df =new_df
    
    if region :
        filtered_df = filtered_df[filtered_df['région'] == region]
        filtered_df['région']

    if aspiration :
        print("hello")
        filtered_df = filtered_df[filtered_df['Categorie_y'] == aspiration]
    
    


    if diplome == "bac" or diplome == "bac_1" or diplome == "bac_2":
        filtered_df = filtered_df[filtered_df['Niveau attendu'] != "bac+3"]

    table = create_table(filtered_df)
    
    

    return table, {"display": "block"}








# @app.callback(
#     Output("score-feedback", "children"),
#     Output("score-feedback", "style"),
#     Input("riasec-score", "value")
# )
# def validate_score(value):
#     # Style par défaut (invisible)
#     default_style = {"color": "red", "fontSize": "12px", "marginTop": "3px", "minHeight": "16px", "visibility": "hidden"}
    
#     if value is None or value == "":
#         return "", default_style  # Garde l'espace sans afficher d'erreur

#     if not value.isdigit():
#         return "❌ Le score doit être un nombre de 6 chiffres.", {**default_style, "visibility": "visible"}

#     if len(value) != 3:
#         return "❌ Le score doit contenir exactement 3 chiffres.", {**default_style, "visibility": "visible"}

#     return "✅ Score valide !", {"color": "green", "fontSize": "12px", "marginTop": "3px", "minHeight": "16px", "visibility": "visible"}



if __name__ == '__main__':
    app.run_server(debug=True)
