import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title='🚀 Athlète Pro Tracker', layout='wide')
st.title('🏋️ Athlète Pro Tracker')

@st.cache_data
def load_data():
    try:
        return pd.read_csv('data.csv')
    except:
        return pd.DataFrame(columns=["Date", "Bloc", "Séance", "Exercice", "Set", "Charge", "Répétitions", "Tempo", "Repos", "RPE", "Technique"])

def save_data(df):
    df.to_csv('data.csv', index=False)

data = load_data()

bloc = st.selectbox("Choisir le Bloc", ["Hypertrophie", "Force", "Métabolique", "Décharge"])
seance = st.selectbox("Sélectionner la Séance", ["Séance 1", "Séance 2", "Séance 3"])

exercices_principaux = ["Squat profond", "Développé couché haltères", "Tractions lestées neutres", "Soulevé de terre roumain", "Développé incliné haltères", "Rowing haltère unilatéral", "Front Squat", "Développé décliné haltères", "Back Squat", "Développé couché barre", "Tractions lestées", "Deadlift traditionnel", "Développé incliné barre", "Rowing Pendlay lourd barre", "Front Squat lourd", "Développé décliné barre lourd"]

# Programme détaillé complet incluant tous les blocs et séances
programme_detaille = {
    "Hypertrophie": {
        "Séance 1": [
            ("Squat profond", 4, "8-10", "3-0-1-0", "90s", "Aucune"),
            ("Développé couché haltères", 4, "8-10", "3-0-1-0", "90s", "Rest-Pause dernière série"),
            ("Tractions lestées neutres", 4, "8", "3-1-1-0", "90s", "Aucune"),
            ("Fentes marchées haltères", 3, "10-12", "2-0-1-0", "60s", "Drop Set dernière série"),
            ("Élévations latérales haltères", 3, "12-15", "2-0-1-1", "60s", "Drop Set dernière série"),
            ("Oiseau haltères", 3, "12-15", "2-0-1-1", "60s", "Drop Set dernière série"),
            ("Curl marteau haltères", 3, "10-12", "2-0-1-0", "60s", "Rest-Pause dernière série"),
            ("Dips lestés", 3, "10-12", "2-0-1-0", "60s", "Rest-Pause dernière série")
        ],
        "Séance 2": [
            ("Soulevé de terre roumain", 4, "8-10", "3-1-1-0", "90s", "Aucune"),
            ("Développé incliné haltères", 4, "8-10", "3-0-1-0", "90s", "Rest-Pause dernière série"),
            ("Rowing haltère unilatéral", 4, "10-12", "2-1-1-1", "90s", "Drop Set dernière série"),
            ("Hip Thrust", 3, "12-15", "2-0-1-2", "60s", "Myo-Reps dernière série"),
            ("Shrugs haltères", 3, "12-15", "2-0-1-1", "60s", "Drop Set dernière série"),
            ("Face Pull poulie", 3, "12-15", "2-0-1-1", "60s", "Drop Set dernière série"),
            ("Curl EZ barre", 3, "12-15", "2-0-1-0", "60s", "Drop Set dernière série"),
            ("Extensions triceps poulie corde", 3, "12-15", "2-0-1-0", "60s", "Drop Set dernière série")
        ],
        "Séance 3": [
            ("Front Squat", 4, "6-8", "3-0-1-0", "90s", "Aucune"),
            ("Développé décliné haltères", 4, "8-10", "3-0-1-0", "90s", "Rest-Pause dernière série"),
            ("Tirage horizontal poulie basse", 4, "10-12", "2-1-1-1", "90s", "Drop Set dernière série"),
            ("Leg Curl allongé", 3, "12-15", "2-0-1-1", "60s", "Myo-Reps dernière série"),
            ("Développé militaire haltères", 3, "10-12", "2-0-1-0", "60s", "Rest-Pause dernière série"),
            ("Curl incliné haltères", 3, "12-15", "3-0-1-0", "60s", "Drop Set dernière série"),
            ("Skullcrushers barre EZ", 3, "12-15", "3-0-1-0", "60s", "Drop Set dernière série")
        ]
    },
    "Force": {"Séance 1": [...], "Séance 2": [...], "Séance 3": [...]},
    "Métabolique": {"Séance 1": [...], "Séance 2": [...], "Séance 3": [...]},
    "Décharge": {"Séance 1": "Réduction 50% volume", "Séance 2": "Réduction 50% volume", "Séance 3": "Réduction 50% volume"}
}

with st.form("nouvelle_seance"):
    st.subheader(f"📌 {bloc} - {seance} - {datetime.date.today()}")
    exercice = st.selectbox("Exercice", [exo[0] for exo in programme_detaille[bloc][seance] if isinstance(exo, tuple)])
    set_no = st.number_input("Numéro du set", 1, 10, 1)
    charge = st.number_input("Charge (kg)", 0.0, 500.0, step=0.5)
    repetitions = st.number_input("Répétitions", 1, 50, 10)
    tempo = st.text_input("Tempo", "3-0-1-0")
    repos = st.number_input("Repos (sec)", 10, 300, 90)
    rpe = st.slider("RPE (Difficulté)", 1, 10, 8)
    technique = st.selectbox("Technique d'intensification", ["Aucune", "Rest-Pause", "Drop Set", "Myo-Reps"])
    submitted = st.form_submit_button("✅ Enregistrer ce set")

    if submitted:
        new_data = pd.DataFrame([{"Date": datetime.date.today(), "Bloc": bloc, "Séance": seance, "Exercice": exercice, "Set": set_no, "Charge": charge, "Répétitions": repetitions, "Tempo": tempo, "Repos": repos, "RPE": rpe, "Technique": technique}])
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.success("🎉 Données enregistrées avec succès !")

if st.checkbox("📋 Voir mon Programme complet"):
    st.subheader(f"🗓 Programme Détaillé - {bloc} / {seance}")
    st.table(pd.DataFrame(programme_detaille[bloc][seance], columns=["Exercice", "Sets", "Reps", "Tempo", "Repos", "Technique"]))


