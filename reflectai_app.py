# reflectai_app.py – Aplicație completă ReflectAI

import streamlit as st
import json
import hashlib
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re

# === SETARE PAGINĂ ===
st.set_page_config(page_title="ReflectAI", page_icon="🧠")

# === UTILITARE PAROLĂ ===

USERS_FILE = "utilizatori.json"

def hash_parola(parola):
    return hashlib.sha256(parola.encode()).hexdigest()

def incarca_utilizatori():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salveaza_utilizatori(utilizatori):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(utilizatori, f, ensure_ascii=False, indent=2)

def creeaza_cont(nume, parola, confirmare):
    utilizatori = incarca_utilizatori()
    if nume in utilizatori:
        return False, "Acest nume de utilizator este deja luat."
    if parola != confirmare:
        return False, "Parolele nu se potrivesc."
    utilizatori[nume] = hash_parola(parola)
    salveaza_utilizatori(utilizatori)
    return True, "Cont creat cu succes!"

def autentificare(nume, parola):
    utilizatori = incarca_utilizatori()
    if nume not in utilizatori:
        return False, "Acest cont nu există."
    if utilizatori[nume] != hash_parola(parola):
        return False, "Parolă incorectă."
    return True, "Autentificare reușită."

# === FUNCȚII JURNAL ===

def analizeaza_sentimentul(text):
    pozitive = ["bine", "fericit", "iubesc", "mândru", "curajos", "clar", "entuziasm", "excelent", "plăcut"]
    negative = ["trist", "obosit", "urăsc", "supărat", "dezamăgit", "confuz", "rău", "singur"]
    text = text.lower()
    score = sum(1 for w in text.split() if w in pozitive) - sum(1 for w in text.split() if w in negative)
    label = "Pozitiv" if score > 0 else "Negativ" if score < 0 else "Neutru"
    return [{"label": label, "score": round(abs(score) / max(1, len(text.split())), 2)}]

def salveaza_intrare_jurnal(utilizator, text, rezultat, tema=None):
    nume_fisier = f"journal_{utilizator}.json"
    data = {
        "text": text.strip(),
        "result": rezultat,
        "timestamp": datetime.now().isoformat()
    }
    if tema:
        data["tema"] = tema
    with open(nume_fisier, "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")

def genereaza_rezumat(utilizator):
    nume_fisier = f"journal_{utilizator}.json"
    if not os.path.exists(nume_fisier):
        st.warning("📂 Nu există jurnal pentru acest utilizator.")
        return
    with open(nume_fisier, "r", encoding="utf-8") as f:
        lines = f.readlines()
    text = "\n".join([json.loads(line)["text"] for line in lines])
    propo = re.split(r'[.!?]', text)
    summary = ". ".join(propo[:2]).strip() + "."
    st.subheader("🧠 Rezumat Emoțional")
    st.markdown(summary)

def afiseaza_grafic(utilizator):
    nume_fisier = f"journal_{utilizator}.json"
    try:
        with open(nume_fisier, "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f]
        df = pd.DataFrame([{
            "timestamp": e["timestamp"],
            "score": e["result"][0]["score"],
            "label": e["result"][0]["label"]
        } for e in data])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        fig, ax = plt.subplots()
        for label in df["label"].unique():
            ax.plot(df[df["label"] == label]["timestamp"],
                    df[df["label"] == label]["score"], label=label, marker="o")
        ax.set_title("Evoluția sentimentelor")
        ax.set_xlabel("Timp")
        ax.set_ylabel("Scor")
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Eroare: {e}")

def sterge_jurnal(utilizator):
    nume_fisier = f"journal_{utilizator}.json"
    if os.path.exists(nume_fisier):
        open(nume_fisier, "w", encoding="utf-8").close()
        st.success("🗑️ Jurnalul a fost șters.")
    else:
        st.info("Nu există jurnal pentru acest utilizator.")

# === INTERFAȚĂ ===

pagina = st.sidebar.selectbox("🔐 Pagina", ["Crează cont", "Autentificare", "Jurnal Emoțional"])

if pagina == "Crează cont":
    st.subheader("🆕 Creare cont")
    nume = st.text_input("👤 Nume utilizator")
    parola = st.text_input("🔑 Parolă", type="password")
    confirmare = st.text_input("🔑 Confirmă parola", type="password")
    if st.button("✅ Creează cont"):
        succes, mesaj = creeaza_cont(nume, parola, confirmare)
        if succes:
            st.success(mesaj)
        else:
            st.error(mesaj)

elif pagina == "Autentificare":
    st.subheader("🔐 Autentificare")
    nume = st.text_input("👤 Nume utilizator", key="login_nume")
    parola = st.text_input("🔑 Parolă", type="password", key="login_parola")
    if st.button("🔓 Autentifică-te"):
        succes, mesaj = autentificare(nume, parola)
        if succes:
            st.success(mesaj)
            st.session_state.utilizator = nume
        else:
            st.error(mesaj)

elif pagina == "Jurnal Emoțional":
    if "utilizator" not in st.session_state:
        st.warning("🔐 Te rugăm să te autentifici mai întâi din pagina 'Autentificare'.")
        st.stop()
    
    utilizator = st.session_state.utilizator
    st.subheader(f"📔 Jurnalul tău – {utilizator}")
    
    tema = st.text_input("📝 Tema zilei (opțional)")
    text = st.text_area("✏️ Scrie ce simți:")
    if st.button("📝 Salvează jurnal"):
        if text.strip():
            rezultat = analizeaza_sentimentul(text)
            salveaza_intrare_jurnal(utilizator, text, rezultat, tema)
            st.success("✅ Intrarea a fost salvată!")
    
    st.markdown("---")
    if st.button("🧠 Generează rezumat"):
        genereaza_rezumat(utilizator)
    
    if st.button("📊 Vezi grafic sentimente"):
        afiseaza_grafic(utilizator)
    
    if st.button("🗑️ Șterge jurnal complet"):
        sterge_jurnal(utilizator)
