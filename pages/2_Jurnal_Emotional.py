import streamlit as st
from datetime import datetime
import json
import random
import os
import re
from collections import Counter

# === Citate motivaționale
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

# === Stil
st.markdown("""
    <style>
        .stApp { background-color: #F6F8FC; }
        h1 { color: #5A4FCF; font-size: 2.8em; text-align: center; }
        .intro { text-align: center; font-size: 1.1em; margin-bottom: 2em; color: #555; }
        .result-box { background-color: #EAF5EA; padding: 1.2em; border-left: 6px solid #4CAF50;
                      margin-top: 1.5em; border-radius: 10px; color: #2E7D32; }
    </style>
""", unsafe_allow_html=True)

# === Titlu și citat
st.markdown("<h1>📘 Jurnal Emoțional</h1>", unsafe_allow_html=True)
st.markdown('<p class="intro">Scrie ce simți. Reflectă. Află ce emoții trăiești.</p>', unsafe_allow_html=True)
st.info(f"💬 {random.choice(quotes)}")

# === Utilizatori
utilizatori_path = "utilizatori.json"
if not os.path.exists(utilizatori_path) or os.path.getsize(utilizatori_path) == 0:
    with open(utilizatori_path, "w", encoding="utf-8") as f:
        json.dump({"alexandru": {"parola": "parolamea"}}, f, indent=2)

try:
    with open(utilizatori_path, "r", encoding="utf-8") as f:
        users = json.load(f)
except Exception:
    st.error("⚠️ Fișierul 'utilizatori.json' e invalid.")
    st.stop()

if "utilizator" not in st.session_state:
    st.error("⚠️ Niciun utilizator autentificat. Te rog loghează-te mai întâi.")
    st.stop()

current_user = st.session_state["utilizator"]

# === Avatar
AVATAR_FOLDER = "avatars"
os.makedirs(AVATAR_FOLDER, exist_ok=True)
avatar_path = os.path.join(AVATAR_FOLDER, f"{current_user}.jpg")

st.markdown("---")
st.subheader("👤 Avatarul tău")

if os.path.exists(avatar_path):
    st.image(avatar_path, width=100, caption="Avatarul tău actual")

uploaded_avatar = st.file_uploader("Încarcă o imagine (JPG/PNG)", type=["jpg", "jpeg", "png"])
if uploaded_avatar:
    with open(avatar_path, "wb") as f:
        f.write(uploaded_avatar.read())
    st.success("✅ Avatar actualizat!")
    st.image(avatar_path, width=100, caption="Avatarul tău nou")

# === Fișier jurnal
user_file = f"jurnale/{current_user}_journal.json"
os.makedirs("jurnale", exist_ok=True)

# === UI
titlu_zi = st.text_input("🗓️ Titlul zilei")
continut = st.text_area("✍️ Ce s-a întâmplat azi în viața ta?", height=200)

col1, col2, col3 = st.columns(3)
with col1:
    analiza_btn = st.button("🔍 Analizează")
with col2:
    save_btn = st.button("💾 Salvează jurnalul")
with col3:
    delete_btn = st.button("🗑️ Șterge istoricul")

# === Dicționar de cuvinte corecte de bază
cuvinte_corecte = set([
    "azi", "mâine", "viața", "titlu", "jurnal", "scris", "ce", "s-a", "întâmplat",
    "este", "o", "zi", "bună", "te", "rog", "scrie", "emoții", "emoțională", "claritate",
    "pas", "reflectă", "emoțional", "interioară", "poveste", "scrisul", "sufletului",
])

# === Funcție analiză text
def analiza_text(text):
    cuvinte = re.findall(r'\b\w+\b', text.lower())
    numar_cuvinte = len(cuvinte)
    numar_fraze = text.count('.') + text.count('!') + text.count('?')
    cuvinte_repetate = {c: n for c, n in Counter(cuvinte).items() if n > 1}
    greseli = [c for c in cuvinte if c not in cuvinte_corecte]
    return numar_cuvinte, numar_fraze, cuvinte_repetate, list(set(greseli))

# === ANALIZA
if analiza_btn:
    if not continut.strip():
        st.warning("Te rog scrie ceva înainte să analizezi.")
    else:
        numar_cuvinte, numar_fraze, cuvinte_repetate, greseli = analiza_text(continut)

        st.success(f"📝 Ai scris **{numar_cuvinte}** cuvinte în **{numar_fraze}** fraze.")

        if cuvinte_repetate:
            st.info("🔁 Cuvinte repetate:")
            for cuv, cnt in cuvinte_repetate.items():
                st.write(f"- **{cuv}** apare de {cnt} ori")

        if greseli:
            st.warning("❌ Posibile greșeli de ortografie:")
            st.write(", ".join(greseli))
        else:
            st.success("✅ Nicio greșeală ortografică identificată.")

        st.markdown("> ✨ *Continua să scrii zilnic. Fiecare cuvânt te aduce mai aproape de claritate.*")

# === SALVARE
if save_btn and continut.strip():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {"data": now, "titlu": titlu_zi, "continut": continut}

    if os.path.exists(user_file):
        with open(user_file, "r", encoding="utf-8") as f:
            jurnal = json.load(f)
    else:
        jurnal = []

    jurnal.append(entry)
    with open(user_file, "w", encoding="utf-8") as f:
        json.dump(jurnal, f, indent=2, ensure_ascii=False)

    st.markdown("""<div class="result-box">✅ Jurnalul a fost salvat! Ai făcut un pas spre înțelegerea ta interioară. 📘<br><br><b>Felicitări!</b> Fiecare zi e diferită. Azi ai ales să fii prezent.</div>""", unsafe_allow_html=True)

# === ȘTERGERE
if delete_btn:
    if os.path.exists(user_file):
        os.remove(user_file)
        st.success("🧹 Istoricul jurnalului a fost șters complet.")
    else:
        st.warning("⚠️ Nu există jurnal salvat.")
