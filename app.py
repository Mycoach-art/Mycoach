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
        "Séance 1": [("Squat profond", "Aucune"), ("Développé couché haltères", "Rest-Pause dernière série"), ("Tractions lestées neutres", "Aucune"), ("Fentes marchées haltères", "Drop Set dernière série"), ("Élévations latérales haltères", "Drop Set dernière série"), ("Oiseau haltères", "Drop Set dernière série"), ("Curl marteau haltères", "Rest-Pause dernière série"), ("Dips lestés", "Rest-Pause dernière série")],
        "Séance 2": [("Soulevé de terre roumain", "Aucune"), ("Développé incliné haltères", "Rest-Pause dernière série"), ("Rowing haltère unilatéral", "Drop Set dernière série"), ("Hip Thrust", "Myo-Reps dernière série"), ("Shrugs haltères", "Drop Set dernière série"), ("Face Pull poulie", "Drop Set dernière série"), ("Curl EZ barre", "Drop Set dernière série"), ("Extensions triceps poulie corde", "Drop Set dernière série")],
        "Séance 3": [("Front Squat", "Aucune"), ("Développé décliné haltères", "Rest-Pause dernière série"), ("Tirage horizontal poulie basse", "Drop Set dernière série"), ("Leg Curl allongé", "Myo-Reps dernière série"), ("Développé militaire haltères", "Rest-Pause dernière série"), ("Curl incliné haltères", "Drop Set dernière série"), ("Skullcrushers barre EZ", "Drop Set dernière série")]
    },
    "Force": {
        "Séance 1": [("Back Squat", "Aucune"), ("Développé couché barre", "Aucune"), ("Tractions lestées", "Aucune"), ("Split Squat bulgare", "Aucune"), ("Développé militaire debout barre", "Aucune"), ("Curl haltères alternés", "Aucune")],
        "Séance 2": [("Deadlift traditionnel", "Aucune"), ("Développé incliné barre", "Aucune"), ("Rowing Pendlay lourd barre", "Aucune"), ("Glute bridge barre", "Aucune"), ("Face Pull lourd poulie", "Aucune"), ("Curl marteau lourd", "Aucune")],
        "Séance 3": [("Front Squat lourd", "Aucune"), ("Développé décliné barre lourd", "Aucune"), ("Tirage horizontal haltère lourd", "Aucune"), ("Leg Curl assis", "Aucune"), ("Épaulé-jeté haltères", "Aucune"), ("Curl barre EZ lourd", "Aucune"), ("Extensions triceps poulie lourd", "Aucune")]
    },
    "Métabolique": {
        "Séance 1": [("Goblet Squat", "Drop Set"), ("Développé couché haltères tempo lent", "Drop Set"), ("Lat Pulldown", "Drop Set"), ("Leg Extension", "Myo-Reps"), ("Élévations latérales haltères", "Drop Set"), ("Oiseau haltères", "Drop Set"), ("Curl concentré haltères", "Drop Set"), ("Pushdown triceps poulie", "Drop Set")],
        "Séance 2": [("Romanian Deadlift tempo lent", "Myo-Reps"), ("Développé incliné haltères haute rep", "Drop Set"), ("Rowing machine tempo lent", "Drop Set"), ("Hip Thrust haute rep", "Myo-Reps"), ("Shrugs haltères", "Drop Set"), ("Face Pull poulie", "Drop Set"), ("Curl haltère incliné", "Drop Set"), ("Extension triceps overhead corde", "Drop Set")],
        "Séance 3": [("Front Squat léger haute rep", "Drop Set"), ("Push-ups lestés haute rep", "Drop Set"), ("Tirage horizontal poulie haute rep", "Drop Set"), ("Leg Curl léger tempo lent", "Myo-Reps"), ("Développé haltères Arnold", "Drop Set"), ("Curl marteau corde", "Drop Set"), ("Kickback triceps poulie", "Drop Set")]
    }
}

if st.checkbox("📋 Voir le Programme Détaillé"):
    st.subheader(f"Programme détaillé - {bloc} / {seance}")
    st.table(pd.DataFrame(programme_detaille[bloc][seance], columns=["Exercice", "Technique Intensification"]))

# Reste du code inchangé...

