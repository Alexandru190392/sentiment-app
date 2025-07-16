import streamlit as st
from datetime import datetime
import json
import random
import os

# Citate despre jurnal
quotes = [
    "Un jurnal nu e doar despre trecut – e despre viitorul tău emoțional.",
    "Scrisul e oglinda sufletului tău în fiecare zi.",
    "Fiecare rând scris e un pas spre claritate interioară.",
    "Nu există zile obișnuite când le transformi în povești.",
    "Jurnalul este prietenul care nu întrerupe niciodată.",
    "Când nu știi ce simți, scrisul îți răspunde.",
    "Jurnalul îți oferă răgazul de a te asculta.",
    "În jurnal, nu există greșeli, doar revelații.",
    "Uneori, hârtia te înțelege mai bine decât oamenii.",
    "Scrisul zilnic e exercițiul tău de sănătate emoțională.",
    # Poți adăuga mai multe aici...
]

# Stil CSS ReflectAI
st.markdown("""
    <style>
        .stApp {
            background-color: #F6F8FC;
        }
        h1 {
            color: #5A4FCF;
            font-size: 2.8em;
            text-align: center;
        }
        .intro {
            text-align: center;
            font-size: 1.1em;
            margin-bottom: 2em;
            color: #555;
        }
        .journal-box {
            background-color: white;
            padding: 2em;
            border-radius: 15px;
            max-width: 700px;
            margin: auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }
        .result-box {
            background-color: #EAF5EA;
            padding: 1.2em;
            border-left: 6px solid #4CAF50;
            margin-top: 1.5em;
            border-radius: 10px;
            color: #2E7D32;
        }
    </style>
""", unsafe_allow_html=True)

# Titlu principal
st.markdown("<h1>📘 Jurnal Emoțional</h1>", unsafe_allow_html=True)
st.markdown('<p class="intro">Scrie ce simți. Reflectă. Află ce emoții trăiești.</p>', unsafe_allow_html=True)

# Citat aleatoriu
st.info(f"💬 {random.choice(quotes)}")

# Load utilizator (exemplu simplu)
with open("utilizatori.json", "r", encoding="utf-8") as f:
    users = json.load(f)

# Selectează utilizatorul activ (aici alegem primul pentru demo)
current_user = list(users.keys())[0]
user_file = f"jurnale/{current_user}_journal.json"

# Creează folder dacă nu există
os.makedirs("jurnale", exist_ok=True)

# Form jurnal
with st.form("jurnal_form"):
    st.markdown('<div class="journal-box">', unsafe_allow_html=True)
    
    titlu_zi = st.text_input("🗓️ Titlul zilei")
    text_input = st.text_area("✍️ Ce s-a întâmplat azi în viața ta?", height=200)
    submitted = st.form_submit_button("🔍 Analizează")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Acțiune la trimitere
if submitted and text_input.strip():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {
        "data": now,
        "titlu": titlu_zi,
        "continut": text_input
    }

    # Încarcă jurnal existent
    if os.path.exists(user_file):
        with open(user_file, "r", encoding="utf-8") as f:
            jurnal = json.load(f)
    else:
        jurnal = []

    # Adaugă în jurnal și salvează
    jurnal.append(entry)
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(jurnal, f, indent=2, ensure_ascii=False)

    st.markdown("""
        <div class="result-box">
            ✅ Jurnalul a fost salvat! Ai făcut un pas spre înțelegerea ta interioară. 📘
            <br><br><b>Felicitări!</b> Fiecare zi e diferită. Azi ai ales să fii prezent.
        </div>
    """, unsafe_allow_html=True)
