import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from PIL import Image

st.set_page_config(page_title="Clasament ReflectAI", page_icon="🏆")
st.title("🏆 Clasament ReflectAI")
st.markdown("Competiția sănătoasă începe! Vezi cine a fost consecvent și cât a scris.")

JOURNAL_FOLDER = "jurnale"
AVATAR_FOLDER = "avatars"

if not os.path.exists(JOURNAL_FOLDER):
    st.warning("📁 Folderul 'jurnale/' nu există.")
    st.stop()

fisiere = [f for f in os.listdir(JOURNAL_FOLDER) if f.endswith("_journal.json")]

if not fisiere:
    st.info("📭 Nu există jurnale salvate încă.")
    st.stop()

clasament = []

def calculeaza_medalie(zile_active):
    if zile_active >= 30:
        return "💎 Diamant"
    elif zile_active >= 14:
        return "🥇 Aur"
    elif zile_active >= 7:
        return "🥈 Argint"
    elif zile_active >= 3:
        return "🥉 Bronz"
    else:
        return "🪙 Început"

for fisier in fisiere:
    username = fisier.replace("_journal.json", "")
    cale = os.path.join(JOURNAL_FOLDER, fisier)

    try:
        with open(cale, "r", encoding="utf-8") as f:
            entries = json.load(f)

        if not entries:
            continue

        cuvinte_total = sum(len(entry["continut"].split()) for entry in entries)
        intrari_total = len(entries)

        zile = set(datetime.strptime(entry["data"], "%Y-%m-%d %H:%M").date() for entry in entries)
        zile_active = len(zile)
        medalie = calculeaza_medalie(zile_active)

        avatar_path = os.path.join(AVATAR_FOLDER, f"{username}.jpg")
        if os.path.exists(avatar_path):
            avatar_img = Image.open(avatar_path)
        else:
            avatar_img = None

        clasament.append({
            "avatar": avatar_img,
            "username": username,
            "medalie": medalie,
            "zile_active": zile_active,
            "cuvinte": cuvinte_total,
            "intrari": intrari_total
        })

    except Exception as e:
        st.error(f"Eroare la procesarea fișierului pentru {username}: {e}")

clasament = sorted(clasament, key=lambda x: x["cuvinte"], reverse=True)

st.markdown("## 🔢 Clasament general:")

for i, persoana in enumerate(clasament):
    # Fundal în funcție de loc
    if i == 0:
        st.markdown("### 🥇 Locul 1")
        bg_color = "#FFFACD"  # Auriu
    elif i == 1:
        st.markdown("### 🥈 Locul 2")
        bg_color = "#E0E0E0"  # Argintiu
    elif i == 2:
        st.markdown("### 🥉 Locul 3")
        bg_color = "#FFDAB9"  # Bronz
    else:
        bg_color = "#F9F9F9"

    with st.container():
        st.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:10px; border-radius:10px; margin-bottom:10px;">
            <div style="display:flex; align-items:center;">
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 2])
        with col1:
            if persoana["avatar"]:
                st.image(persoana["avatar"], width=60)
            else:
                st.markdown("🧑")
        with col2:
            st.markdown(f"**{persoana['username']}**")
        with col3:
            st.markdown(persoana["medalie"])
        with col4:
            st.markdown(f"🔥 {persoana['zile_active']} zile")
        with col5:
            st.markdown(f"✍️ {persoana['cuvinte']} cuvinte | 📘 {persoana['intrari']} intrări")

        st.markdown("</div></div>", unsafe_allow_html=True)
