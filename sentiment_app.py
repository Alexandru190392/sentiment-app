import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import re

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

def salveaza_intrare_jurnal(text, rezultat, tema=None):
    data = {"text": text.strip(), "result": rezultat, "timestamp": datetime.now().isoformat()}
    if tema:
        data["tema"] = tema
    with open("journal_entries.json", "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")

def afiseaza_grafic_sentimente():
    try:
        with open("result.json", "r", encoding="utf-8") as f:
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

def genereaza_rezumat_emotional():
    try:
        if not os.path.exists("journal_entries.json"):
            st.warning("Nu există date.")
            return
        with open("journal_entries.json", "r", encoding="utf-8") as f:
            lines = f.readlines()
        text = "\n".join([json.loads(line)["text"] for line in lines])
        propoziții = re.split(r'[.!?]', text)
        summary = ". ".join(propoziții[:2]).strip() + "."
        st.subheader("🧠 Rezumat Emoțional (Logic)")
        st.markdown(summary)
    except Exception as e:
        st.error(f"Eroare la rezumat: {e}")

# === INTERFAȚĂ ===
st.title("🔍 ReflectAI - Varianta DEMO (Rapidă și Offline)")

if st.button("📈 Vezi graficul cu evoluția sentimentelor"):
    afiseaza_grafic_sentimente()

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

st.header("📓 Emotional Journal – Reflect and Grow")
with st.form("journal_form"):
    tema = st.text_input("Optional: Tema zilei")
    jurnal_text = st.text_area("Scrie ce simți:", height=300)
    submit = st.form_submit_button("📝 Salvează jurnal")
if submit and jurnal_text.strip():
    rezultat = analizeaza_sentimentul(jurnal_text)
    salveaza_intrare_jurnal(jurnal_text, rezultat, tema)
    st.success(f"✅ Jurnal salvat — {rezultat[0]['label']} ({rezultat[0]['score']:.4f})")

if st.button("🧠 Generează Rezumat Emoțional"):
    genereaza_rezumat_emotional()
