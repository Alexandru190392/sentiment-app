import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="Panou Administrare", page_icon="🛠️")

st.title("🛠️ Panou de Administrare ReflectAI")
st.markdown("Vezi toți utilizatorii și statisticile lor de jurnal.")

JOURNAL_FOLDER = "jurnale"

if not os.path.exists(JOURNAL_FOLDER):
    st.warning("📁 Folderul 'jurnale/' nu există încă.")
    st.stop()

fisiere = [f for f in os.listdir(JOURNAL_FOLDER) if f.endswith("_journal.json")]

if not fisiere:
    st.info("📭 Nu există niciun jurnal salvat momentan.")
    st.stop()

date_useri = []

for fisier in fisiere:
    nume_user = fisier.replace("_journal.json", "")
    cale = os.path.join(JOURNAL_FOLDER, fisier)
    try:
        with open(cale, "r", encoding="utf-8") as f:
            intrari = json.load(f)
            nr_intrari = len(intrari)

            if nr_intrari > 0:
                ultima_data = intrari[-1]["data"]
                titlu_ultim = intrari[-1].get("titlu", "(fără titlu)")
            else:
                ultima_data = "-"
                titlu_ultim = "-"

            date_useri.append({
                "Utilizator": nume_user,
                "Intrări în jurnal": nr_intrari,
                "Ultima salvare": ultima_data,
                "Ultimul titlu": titlu_ultim
            })
    except Exception as e:
        st.error(f"❌ Eroare la citirea fișierului pentru {nume_user}: {e}")

# ✅ Afișează tabel
st.dataframe(date_useri, use_container_width=True)
