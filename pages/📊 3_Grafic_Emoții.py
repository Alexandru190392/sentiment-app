import streamlit as st
import os
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import Counter
import re

st.set_page_config(page_title="Grafic Emoții", page_icon="📈")
st.title("📈 Evoluția Emoțiilor")

PERIOADE = {
    "Ultima oră": timedelta(hours=1),
    "Ultima zi": timedelta(days=1),
    "Ultimele 2 zile": timedelta(days=2),
    "Ultima săptămână": timedelta(weeks=1),
    "Ultima lună": timedelta(days=30),
    "Ultimul an": timedelta(days=365),
}

optiune = st.selectbox("Selectează perioada pentru analiză:", list(PERIOADE.keys()))

JOURNAL_FOLDER = "jurnale"
if "utilizator" not in st.session_state:
    st.warning("Te rog autentifică-te mai întâi.")
    st.stop()

current_user = st.session_state["utilizator"]
cale_jurnal = os.path.join(JOURNAL_FOLDER, f"{current_user}_journal.json")

if not os.path.exists(cale_jurnal):
    st.info("Nu există jurnale salvate pentru acest utilizator.")
    st.stop()

try:
    with open(cale_jurnal, "r", encoding="utf-8") as f:
        jurnal = json.load(f)
except:
    st.error("Eroare la citirea fișierului jurnal.")
    st.stop()

# === Extrage emoții (extins) ===
def extrage_emoții(text):
    emotii = {
        "fericit": ["fericit", "bucurie", "entuziasm", "recunoscător", "încântat", "satisfăcut", "mândru", "optimist"],
        "trist": ["trist", "melancolic", "pierdut", "plâns", "dezamăgit", "abătut", "nefericit"],
        "nervos": ["nervos", "furios", "supărat", "iritat", "enervat", "agitat", "exasperat"],
        "îngrijorat": ["îngrijorat", "anxios", "temător", "nesigur", "fricos", "tensionat", "neliniștit"],
        "calm": ["calm", "liniște", "pace", "relaxat", "echilibrat", "clar", "seren"],
        "confuz": ["confuz", "derutat", "neclar", "ambiguu", "dezorientat"],
        "iubit": ["iubit", "acceptat", "sprijinit", "împărtășit", "conectat"],
        "singur": ["singur", "izolat", "neînțeles", "respins", "părăsit"],
        "curajos": ["curajos", "hotărât", "puternic", "neînfricat", "rezilient"],
        "rușinat": ["rușinat", "jenat", "vinovat", "stânjenit"]
    }
    count = Counter()
    cuvinte = re.findall(r'\b\w+\b', text.lower())
    for emotie, chei in emotii.items():
        count[emotie] += sum(cuvinte.count(cuv) for cuv in chei)
    return count

# === Filtrare în funcție de perioada selectată ===
perioada_aleasa = PERIOADE[optiune]
acum = datetime.now()

emoții_total = Counter()
for intrare in jurnal:
    try:
        data = datetime.strptime(intrare["data"], "%Y-%m-%d %H:%M")
    except:
        continue
    if acum - data <= perioada_aleasa:
        continut = intrare.get("continut", "")
        emoții_total += extrage_emoții(continut)

if not emoții_total:
    st.info("Nu au fost detectate emoții în perioada selectată.")
    st.stop()

# === Afișare grafice ===
st.markdown("### Distribuția Emoțiilor:")
labels = list(emoții_total.keys())
valori = list(emoții_total.values())

fig, ax = plt.subplots()
ax.pie(valori, labels=labels, autopct="%1.1f%%", startangle=90)
ax.axis('equal')
st.pyplot(fig)

# === Legendă simplă ===
st.markdown("---")
st.markdown("**📊 Emoții detectate:**")
for emotie, val in emoții_total.items():
    st.write(f"- {emotie.capitalize()}: {val} mențiuni")
