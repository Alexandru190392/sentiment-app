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
]

# Stil CSS
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

# Titlu și citat
st.markdown("<h1>📘 Jurnal Emoțional</h1>", unsafe_allow_html=True)
st.markdown('<p class="intro">Scrie ce simți. Reflectă. Află ce emoții trăiești.</p>', unsafe_allow_html=True)
st.info(f"💬 {random.choice(quotes)}")

# Autentificare și citire utilizator
utilizatori_path = "utilizatori.json"
if not os.path.exists(utilizatori_path) or os.path.getsize(utilizatori_path) == 0:
    default_users = {
        "alexandru": {
            "parola": "parolamea"
        }
    }
    with open(utilizatori_path, "w", encoding="utf-8") as f:
        json.dump(default_users, f, indent=2, ensure_ascii=False)

try:
    with open(utilizatori_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            raise ValueError("Fișier gol")
        users = json.loads(content)
except Exception:
    st.error("⚠️ Fișierul 'utilizatori.json' este gol, invalid sau corupt. Te rog adaugă cel puțin un utilizator.")
    st.stop()

if not users or not isinstance(users, dict):
    st.error("⚠️ Fișierul 'utilizatori.json' nu conține un dicționar de utilizatori.")
    st.stop()

if "utilizator" not in st.session_state:
    st.error("⚠️ Niciun utilizator autentificat. Te rog loghează-te mai întâi.")
    st.stop()

current_user = st.session_state["utilizator"]
# === Upload Avatar ===
AVATAR_FOLDER = "avatars"
os.makedirs(AVATAR_FOLDER, exist_ok=True)

st.markdown("---")
st.subheader("👤 Avatarul tău")

avatar_path = os.path.join(AVATAR_FOLDER, f"{current_user}.jpg")

# Afișăm avatarul curent dacă există
if os.path.exists(avatar_path):
    st.image(avatar_path, width=100, caption="Avatarul tău actual")

# Upload nou
uploaded_avatar = st.file_uploader("Încarcă o imagine (JPG/PNG)", type=["jpg", "jpeg", "png"])
if uploaded_avatar is not None:
    with open(avatar_path, "wb") as f:
        f.write(uploaded_avatar.read())
    st.success("✅ Avatar actualizat!")
    st.image(avatar_path, width=100, caption="Avatarul tău nou")
user_file = f"jurnale/{current_user}_journal.json"
os.makedirs("jurnale", exist_ok=True)

# UI principal (fără div extra care crea spațiu alb)
titlu_zi = st.text_input("🗓️ Titlul zilei")
text_input = st.text_area("✍️ Ce s-a întâmplat azi în viața ta?", height=200)

# Butoane
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    analiza_btn = st.button("🔍 Analizează")
with col2:
    save_btn = st.button("💾 Salvează jurnalul")
with col3:
    delete_btn = st.button("🗑️ Șterge istoricul")

# Analiză cuvânt
if analiza_btn:
    word_count = len(text_input.split())
    st.markdown(f"""
        <div class="result-box">
            🔍 Ai scris <b>{word_count} cuvinte</b> azi. Fiecare cuvânt te apropie mai mult de tine.
            <br><br><b>Continuă!</b> Reflecția zilnică este cheia emoțională a maturității.
        </div>
    """, unsafe_allow_html=True)

# Salvare jurnal
if save_btn and text_input.strip():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {"data": now, "titlu": titlu_zi, "continut": text_input}

    if os.path.exists(user_file):
        with open(user_file, "r", encoding="utf-8") as f:
            jurnal = json.load(f)
    else:
        jurnal = []

    jurnal.append(entry)
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(jurnal, f, indent=2, ensure_ascii=False)

    st.markdown("""
        <div class="result-box">
            ✅ Jurnalul a fost salvat! Ai făcut un pas spre înțelegerea ta interioară. 📘
            <br><br><b>Felicitări!</b> Fiecare zi e diferită. Azi ai ales să fii prezent.
        </div>
    """, unsafe_allow_html=True)

# Ștergere istoric
if delete_btn:
    if os.path.exists(user_file):
        os.remove(user_file)
        st.success("🧹 Istoricul jurnalului a fost șters complet.")
    else:
        st.warning("⚠️ Nu există jurnal salvat.")
