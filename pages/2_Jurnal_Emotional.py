import streamlit as st
from datetime import datetime
import json
import random
import os
import re
from collections import Counter

# === Citate motivaționale
quotes = [
    "Ești mai puternic decât crezi. Scrisul tău o dovedește.",
    "Chiar și azi, cu toate greutățile, ai ales să fii prezent.",
    "Respiră. Scrie. Încet, lucrurile se vor așeza.",
    "Nu trebuie să ai totul sub control. E suficient să fii aici.",
    "Ai trecut prin multe, dar încă ești în picioare. Asta înseamnă curaj.",
    "Scrisul tău e o dovadă că nu renunți.",
    "E ok să te simți obosit. Nu renunța. Te refaci pas cu pas.",
    "Jurnalul e spațiul tău sigur. Aici ești acceptat complet.",
    "Uneori, doar faptul că scrii înseamnă că alegi vindecarea.",
    "Ești exact unde trebuie să fii pentru a începe să te înțelegi.",
    "Fiecare cuvânt scris e un pas către mai bine.",
    "Nu e nevoie să fii puternic azi. E de ajuns că ești sincer.",
    "Ai voie să cazi. Și ai dreptul să te ridici, în ritmul tău.",
    "Ce simți nu e greșit. E real. Și are locul lui aici.",
    "Fii blând cu tine. Ai făcut tot ce ai putut, cu ce ai avut.",
    "Scrisul e modul tău de a-ți aminti că meriți să fii bine.",
    "Dacă citești asta, înseamnă că nu ai renunțat. Și asta e măreț.",
    "Azi nu trebuie să fii perfect. Doar să fii.",
    "Nu te judeca. Creșterea începe cu înțelegere, nu cu critică.",
    "Ești demn de iubire și înțelegere, chiar și în zilele grele.",
    "Durerea de azi poate deveni înțelepciunea de mâine.",
    "Tu contezi. Ce simți contează. Ce scrii aici contează.",
    "Fiecare zi în care scrii e o zi în care ai ales să ai grijă de tine.",
    "Te descurci. Chiar și când simți că nu, ai făcut un pas azi.",
    "Încă ești aici. Și asta spune totul despre tine.",
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
def analiza_extinsa(text):
    cuvinte = re.findall(r'\b\w+\b', text.lower())
    numar_total = len(cuvinte)
    numar_fraze = len(re.findall(r'[.!?]', text))
    cuvinte_repetate = {c: n for c, n in Counter(cuvinte).items() if n > 1}
    greseli = [c for c in cuvinte if c not in cuvinte_corecte]
    corecte = [c for c in cuvinte if c in cuvinte_corecte]
    procent_corect = int((len(corecte) / numar_total) * 100) if numar_total > 0 else 0

    fraze_inspirationale = []
    fraze = re.split(r'[.!?]', text)
    for fraza in fraze:
        if len(fraza.split()) > 4 and any(word in fraza.lower() for word in [
            "vis", "speranță", "putere", "curaj", "iubire", "libertate", "cred", "merit", "încercare"
        ]):
            fraze_inspirationale.append(fraza.strip())

    return numar_total, numar_fraze, procent_corect, cuvinte_repetate, list(set(greseli)), fraze_inspirationale

# === ANALIZA
if analiza_btn:
    if not continut.strip():
        st.warning("Te rog scrie ceva înainte să analizezi.")
    else:
        numar_cuvinte, numar_fraze, procent_corect, cuvinte_repetate, greseli, fraze_insp = analiza_extinsa(continut)

        st.success(f"📝 Ai scris **{numar_cuvinte}** cuvinte în **{numar_fraze}** fraze.")

        if cuvinte_repetate:
            st.info("🔁 Cuvinte repetate:")
            for cuv, cnt in cuvinte_repetate.items():
                st.write(f"- **{cuv}** apare de {cnt} ori")

        if greseli:
            st.warning(f"❌ Posibile greșeli gramaticale ({100 - procent_corect}% erori):")
            st.write(", ".join(greseli))
        else:
            st.success("✅ Nicio greșeală ortografică identificată.")

        st.info(f"✅ Corectitudine gramaticală estimată: **{procent_corect}%**")

        if fraze_insp:
            st.markdown("✨ **Fraze inspiraționale detectate:**")
            for f in fraze_insp:
                st.write(f"• _{f}_")
        else:
            st.markdown("💡 *Nicio frază inspirațională detectată în această intrare.*")

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
