import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re
import hashlib

def hash_parola(parola):
    return hashlib.sha256(parola.encode()).hexdigest()

def verifica_utilizator(nume, parola):
    if not os.path.exists("users.json"):
        return True  # nu există utilizatori încă

    with open("users.json", "r", encoding="utf-8") as f:
        try:
            users = json.load(f)
        except:
            users = {}

    nume = nume.strip().lower().replace(" ", "_")
    parola_hash = hash_parola(parola)

    if nume in users:
        return users[nume] == parola_hash
    else:
        # utilizator nou -> salvăm parola
        users[nume] = parola_hash
        with open("users.json", "w", encoding="utf-8") as f_out:
            json.dump(users, f_out, ensure_ascii=False, indent=2)
        return True


# === FUNCȚII ===

def analizeaza_sentimentul(text):
    pozitive = ["bine", "fericit", "iubesc", "mândru", "curajos", "clar", "entuziasm", "excelent", "plăcut"]
    negative = ["trist", "obosit", "urăsc", "supărat", "dezamăgit", "confuz", "rău", "singur"]
    text = text.lower()
    score = sum(1 for w in text.split() if w in pozitive) - sum(1 for w in text.split() if w in negative)
    label = "Pozitiv" if score > 0 else "Negativ" if score < 0 else "Neutru"
    return [{"label": label, "score": round(abs(score) / max(1, len(text.split())), 2)}]

def salveaza_rezultatul(text, result):
    data = {"text": text.strip(), "result": result, "timestamp": datetime.now().isoformat()}
    with open("result.json", "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")

def adauga_feedback(feedback):
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} - {feedback}\n")

def salveaza_intrare_jurnal_personalizat(user, text, rezultat, tema=None):
    if not user.strip():
        st.error("⚠️ Trebuie să introduci un nume de utilizator!")
        return
    nume_fisier = f"journal_{user.strip().lower().replace(' ', '_')}.json"
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
    st.success("✅ Intrarea ta a fost salvată cu succes!")

def genereaza_rezumat_emotional(user):
    nume_fisier = f"journal_{user.strip().lower().replace(' ', '_')}.json"
    try:
        if not os.path.exists(nume_fisier):
            st.warning("Nu există date pentru acest utilizator.")
            return
        with open(nume_fisier, "r", encoding="utf-8") as f:
            lines = f.readlines()
        text = "\n".join([json.loads(line)["text"] for line in lines])
        propoziții = re.split(r'[.!?]', text)
        summary = ". ".join(propoziții[:2]).strip() + "."
        st.subheader("🧠 Rezumat Emoțional (Logic)")
        st.markdown(summary)
    except Exception as e:
        st.error(f"Eroare la rezumat: {e}")

def afiseaza_grafic_sentimente(user):
    nume_fisier = f"journal_{user.strip().lower().replace(' ', '_')}.json"
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
            subset = df[df["label"] == label]
            ax.plot(subset["timestamp"], subset["score"], label=label, marker='o')
        ax.set_title("Evoluția sentimentelor în timp")
        ax.set_xlabel("Timp")
        ax.set_ylabel("Scor sentiment")
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"Eroare la încărcarea datelor: {e}")

def sterge_jurnal(user):
    nume_fisier = f"journal_{user.strip().lower().replace(' ', '_')}.json"
    if os.path.exists(nume_fisier):
        open(nume_fisier, "w", encoding="utf-8").close()
        st.warning("⚠️ Jurnalul a fost șters complet.")
    else:
        st.info("📂 Nu există jurnal pentru acest utilizator.")

# === INTERFAȚĂ ===

st.title("🔍 ReflectAI – Varianta Personalizată DEMO")

st.header("📓 Emotional Journal – Reflect and Grow")
with st.form("journal_form"):
    utilizator = st.text_input("👤 Nume utilizator (obligatoriu pentru jurnal)")
    tema = st.text_input("📝 Tema zilei (opțional)")
    jurnal_text = st.text_area("✏️ Scrie ce simți:", height=300)
    submit = st.form_submit_button("📝 Salvează jurnal")

if submit and jurnal_text.strip():
    rezultat = analizeaza_sentimentul(jurnal_text)
    salveaza_intrare_jurnal_personalizat(utilizator, jurnal_text, rezultat, tema)

# === Rezumat & Vizualizare ===

st.subheader("📈 Analizează Jurnalul Tău")
if utilizator.strip():
    if st.button("🧠 Generează Rezumat Emoțional"):
        genereaza_rezumat_emotional(utilizator)

    if st.button("📊 Vezi graficul cu evoluția sentimentelor"):
        afiseaza_grafic_sentimente(utilizator)

    if st.button("🗑️ Șterge toate intrările din jurnal"):
        sterge_jurnal(utilizator)

# === Analiză individuală ===

st.header("💬 Analiză Rapidă Sentiment Text")
text_input = st.text_area("✏️ Introdu textul pentru analiză:")
if st.button("🔍 Analizează"):
    if text_input:
        rezultat = analizeaza_sentimentul(text_input)
        st.success(f"Etichetă: {rezultat[0]['label']} — Scor: {rezultat[0]['score']:.4f}")
        salveaza_rezultatul(text_input, rezultat)
        feedback = st.radio("📊 A fost analiza utilă?", ["Da", "Nu"])
        if st.button("📤 Trimite feedback"):
            adauga_feedback(feedback)
            st.info("✅ Feedback salvat. Mulțumim!")
    else:
        st.warning("Te rugăm să introduci un text.")
