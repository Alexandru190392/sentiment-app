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

        # Zile active (unicitate pe data calendaristică)
        zile = set(datetime.strptime(entry["data"], "%Y-%m-%d %H:%M").date() for entry in entries)
        zile_active = len(zile)
        medalie = calculeaza_medalie(zile_active)

        # Avatar
        avatar_path = os.path.join(AVATAR_FOLDER, f"{username}.jpg")
        if os.path.exists(avatar_path):
            avatar_img = Image.open(avatar_path)
        else:
            avatar_img = None

        clasament.append({
            "avatar": avatar_img,
            "us
