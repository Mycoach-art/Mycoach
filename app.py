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

bloc = st.selectbox("Choisir le Bloc", ["Hypertrophie", "Force", "Métabolique"])
seance = st.selectbox("Sélectionner la Séance", ["Séance 1", "Séance 2", "Séance 3"])

exercices_principaux = ["Squat profond", "Développé couché haltères", "Tractions lestées neutres", "Soulevé de terre roumain", "Développé incliné haltères", "Rowing haltère unilatéral", "Front Squat", "Développé décliné haltères", "Back Squat", "Développé couché barre", "Tractions lestées", "Deadlift traditionnel", "Développé incliné barre", "Rowing Pendlay lourd barre", "Front Squat lourd", "Développé décliné barre lourd"]

programme_detaille = {
    "Hypertrophie": {
        "Séance 1": [
            ("Squat profond", "4", "8-10", "3-0-1-0", "90s", "Aucune"),
            ("Développé couché haltères", "4", "8-10", "3-0-1-0", "90s", "Rest-Pause dernière série"),
            ("Tractions lestées neutres", "4", "8", "3-1-1-0", "90s", "Aucune"),
            ("Fentes marchées haltères", "3", "10-12", "2-0-1-0", "60s", "Drop Set dernière série"),
            ("Élévations latérales haltères", "3", "12-15", "2-0-1-1", "60s", "Drop Set dernière série"),
            ("Oiseau haltères", "3", "12-15", "2-0-1-1", "60s", "Drop Set dernière série"),
            ("Curl marteau haltères", "3", "10-12", "2-0-1-0", "60s", "Rest-Pause dernière série"),
            ("Dips lestés", "3", "10-12", "2-0-1-0", "60s", "Rest-Pause dernière série")
        ],
    },
    # Autres blocs simplifiés pour exemple...
}

with st.form("nouvelle_seance"):
    st.subheader(f"📌 {bloc} - {seance} - {datetime.date.today()}")
    exercice = st.selectbox("Exercice", [exo[0] for exo in programme_detaille[bloc][seance]])
    set_no = st.number_input("Numéro du set", 1, 10, 1)
    charge = st.number_input("Charge (kg)", 0.0, 500.0, step=0.5)
    repetitions = st.number_input("Répétitions", 1, 50, 10)
    tempo = st.text_input("Tempo (ex: 3-0-1-0)", "3-0-1-0")
    repos = st.number_input("Repos (sec)", 10, 300, 90)
    rpe = st.slider("RPE (Difficulté)", 1, 10, 8)
    technique = st.selectbox("Technique d'intensification", ["Aucune", "Rest-Pause", "Drop Set", "Myo-Reps"])

    submitted = st.form_submit_button("✅ Enregistrer ce set")

    if submitted:
        new_data = pd.DataFrame([{
            "Date": datetime.date.today(), "Bloc": bloc, "Séance": seance, "Exercice": exercice,
            "Set": set_no, "Charge": charge, "Répétitions": repetitions, "Tempo": tempo,
            "Repos": repos, "RPE": rpe, "Technique": technique
        }])
        data = pd.concat([data, new_data], ignore_index=True)
        save_data(data)
        st.success("🎉 Données enregistrées avec succès !")

if st.checkbox("📋 Voir mon Programme complet"):
    st.subheader(f"🗓 Programme Détaillé - {bloc} / {seance}")
    programme_df = pd.DataFrame(programme_detaille[bloc][seance], columns=["Exercice", "Sets", "Répétitions", "Tempo", "Repos", "Technique Intensification"])
    st.table(programme_df)

st.subheader("📈 Historique de progression")
st.dataframe(data.tail(10), use_container_width=True)

st.subheader("🎯 Objectifs prochaine séance")
prochaines_charges = {}
for exo in [x[0] for x in programme_detaille[bloc][seance]]:
    exo_data = data[(data["Exercice"] == exo) & (data["Bloc"] == bloc)]
    if not exo_data.empty:
        derniere_charge = exo_data.iloc[-1]["Charge"]
        derniere_rpe = exo_data.iloc[-1]["RPE"]
        progression = 1.025 if exo in exercices_principaux and derniere_rpe <= 8 else 1.015
        prochaine_charge = round(derniere_charge * progression, 1)
        prochaines_charges[exo] = prochaine_charge

if prochaines_charges:
    st.table(pd.DataFrame(prochaines_charges.items(), columns=["Exercice", "Charge Prochaine Séance (kg)"]))
else:
    st.info("Aucune donnée antérieure pour calculer la progression.")

