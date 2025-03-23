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

exercices = {
    "Hypertrophie": {
        "Séance 1": ["Squat profond", "Développé couché haltères", "Tractions lestées neutres", "Fentes marchées haltères", "Élévations latérales haltères", "Oiseau haltères", "Curl marteau haltères", "Dips lestés"],
        "Séance 2": ["Soulevé de terre roumain", "Développé incliné haltères", "Rowing haltère unilatéral", "Hip Thrust", "Shrugs haltères", "Face Pull poulie", "Curl EZ barre", "Extensions triceps poulie corde"],
        "Séance 3": ["Front Squat", "Développé décliné haltères", "Tirage horizontal poulie basse", "Leg Curl allongé", "Développé militaire haltères", "Curl incliné haltères", "Skullcrushers barre EZ"]
    },
    "Force": {
        "Séance 1": ["Back Squat", "Développé couché barre", "Tractions lestées", "Split Squat bulgare", "Développé militaire debout barre", "Curl haltères alternés"],
        "Séance 2": ["Deadlift traditionnel", "Développé incliné barre", "Rowing Pendlay lourd barre", "Glute bridge barre", "Face Pull lourd poulie", "Curl marteau lourd"],
        "Séance 3": ["Front Squat lourd", "Développé décliné barre lourd", "Tirage horizontal haltère lourd", "Leg Curl assis", "Épaulé-jeté haltères", "Curl barre EZ lourd", "Extensions triceps poulie lourd"]
    },
    "Métabolique": {
        "Séance 1": ["Goblet Squat", "Développé couché haltères tempo lent", "Lat Pulldown", "Leg Extension", "Élévations latérales haltères", "Oiseau haltères", "Curl concentré haltères", "Pushdown triceps poulie"],
        "Séance 2": ["Romanian Deadlift tempo lent", "Développé incliné haltères haute rep", "Rowing machine tempo lent", "Hip Thrust haute rep", "Shrugs haltères", "Face Pull poulie", "Curl haltère incliné", "Extension triceps overhead corde"],
        "Séance 3": ["Front Squat léger haute rep", "Push-ups lestés haute rep", "Tirage horizontal poulie haute rep", "Leg Curl léger tempo lent", "Développé haltères Arnold", "Curl marteau corde", "Kickback triceps poulie"]
    }
}

with st.form("nouvelle_seance"):
    st.subheader(f"📌 {bloc} - {seance} - {datetime.date.today()}")
    exercice = st.selectbox("Exercice", exercices[bloc][seance])
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
    st.subheader("🗓 Programme Complet")
    for bloc_name, seances in exercices.items():
        st.write(f"## {bloc_name}")
        for seance_name, exos in seances.items():
            st.write(f"### {seance_name}")
            st.write(", ".join(exos))
        st.write("**Semaine de deload après chaque bloc** (réduction 50% du volume)")

st.subheader("📈 Historique de progression")
st.dataframe(data.tail(10), use_container_width=True)

st.subheader("🎯 Objectifs prochaine séance")
prochaines_charges = {}
for exo in exercices[bloc][seance]:
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
