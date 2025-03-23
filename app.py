import streamlit as st
import pandas as pd
import datetime

# Titre et style gamifié
st.set_page_config(page_title='🚀 Athlète Pro Tracker', layout='wide')
st.title('🏋️ Athlète Pro Tracker')

# Chargement des données
@st.cache_data
def load_data():
    try:
        return pd.read_csv('data.csv')
    except:
        return pd.DataFrame(columns=["Date","Bloc","Séance","Exercice","Set","Charge","Répétitions","Tempo","Repos","RPE","Technique"])

# Sauvegarde des données
def save_data(df):
    df.to_csv('data.csv', index=False)

data = load_data()

# Sélection du bloc
bloc = st.selectbox("Choisir le Bloc", ["Hypertrophie", "Force", "Métabolique"])

# Sélection de la séance
seance = st.selectbox("Sélectionner la Séance", ["Séance 1", "Séance 2", "Séance 3"])

# Exercices prédéfinis
exercices = {
    "Séance 1": ["Squat profond", "Développé couché haltères", "Tractions lestées", "Fentes marchées", "Élévations latérales + Oiseau", "Curl marteau + Dips"],
    "Séance 2": ["Soulevé de terre roumain", "Développé incliné haltères", "Rowing haltère", "Hip Thrust", "Face Pull + Shrugs", "Curl EZ + Extension Triceps"],
    "Séance 3": ["Front Squat", "Développé décliné", "Tirage horizontal", "Leg Curl", "Développé militaire", "Curl incliné + Skullcrushers"]
}

# Formulaire pour enregistrer la séance
with st.form("nouvelle_seance"):
    st.subheader(f"📌 {bloc} - {seance} - {datetime.date.today()}")
    exercice = st.selectbox("Exercice", exercices[seance])
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

# Affichage des performances récentes
st.subheader("📈 Historique de progression")
st.dataframe(data.tail(10), use_container_width=True)

# Calcul progression prochaine séance
st.subheader("🎯 Objectifs prochaine séance")
prochaines_charges = {}
for exo in exercices[seance]:
    exo_data = data[(data["Exercice"] == exo) & (data["Bloc"] == bloc)]
    if not exo_data.empty:
        derniere_charge = exo_data.iloc[-1]["Charge"]
        prochaine_charge = round(derniere_charge * 1.025, 1)
        prochaines_charges[exo] = prochaine_charge

if prochaines_charges:
    st.table(pd.DataFrame(prochaines_charges.items(), columns=["Exercice", "Charge Prochaine Séance (kg)"]))
else:
    st.info("Aucune donnée antérieure pour calculer la progression.")
