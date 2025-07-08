import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter
import re
from scipy.spatial.distance import cosine
import torch

# === CONFIGURARE ===
try:
    from transformers import pipeline
    sentiment_analyzer = pipeline("sentiment-analysis")
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    sentiment_analyzer = None
    summarizer = None
    st.error("❌ Eroare la încărcarea pachetelor 'transformers' sau la inițializare.")

embedding_model = None

# === ÎNCĂRCARE MODEL DE SIMILARITATE LA CERERE ===
def get_embedding_model():
    global embedding_model
    if embedding_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            embedding_model = None
            st.warning("⚠️ Modelul de similaritate nu a fost încărcat. Funcția de comparare este dezactivată.")
    return embedding_model

# === FUNCȚII PRINCIPALE ===
def analizeaza_sentimentul(text):
    if sentiment_analyzer:
        return sentiment_analyzer(text)
    else:
        return [{"label": "N/A", "score": 0.0}]

def salveaza_rezultatul(text, result):
    data = {
        "text": text.strip(),
        "result": result,
        "timestamp": datetime.now().isoformat()
    }
    with open("result.json", "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")

def adauga_feedback(feedback):
    with open("feedback.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} - {feedback}\n")

def salveaza_intrare_jurnal(text, rezultat, tema=None):
    data = {
        "text": text.strip(),
        "result": rezultat,
        "timestamp": datetime.now().isoformat()
    }
    if tema:
        data["tema"] = tema
    with open("journal_entries.json", "a", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        f.write("\n")

def afiseaza_grafic_sentimente():
    try:
        with open("result.json", "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f.readlines()]
        df = pd.DataFrame([{
            "timestamp": entry["timestamp"],
            "score": entry["result"][0]["score"],
            "label": entry["result"][0]["label"]
        } for entry in data])
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
        st.warning(f"Nu s-au putut încărca datele. Detalii: {e}")

# === INTERFAȚĂ STREAMLIT ===
st.title("🔍 Analiză Sentiment - Demo Alexandru Florin Drăghici")

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
    tema_zilei = st.text_input("Optional: Today's topic")
    text_jurnal = st.text_area("Scrie ce simți:", height=300)
    submit = st.form_submit_button("📝 Save Journal")
if submit and text_jurnal.strip():
    rezultat = analizeaza_sentimentul(text_jurnal)
    salveaza_intrare_jurnal(text_jurnal, rezultat, tema_zilei)
    st.success(f"✅ Journal saved — Label: {rezultat[0]['label']}, Score: {rezultat[0]['score']:.4f}")

if st.button("🔎 Deep Research – Analyze your journal"):
    st.warning("🔧 Funcția de comparare nu este activată momentan din cauza modelului de similaritate.")

if st.button("🧠 Generate Emotional Summary"):
    try:
        if not os.path.exists("journal_entries.json"):
            st.warning("No journal data found.")
        else:
            with open("journal_entries.json", "r", encoding="utf-8") as f:
                lines = f.readlines()
            full_text = "\n".join([json.loads(line)["text"] for line in lines])
            if len(full_text) > 3000:
                full_text = full_text[:3000]
            summary = summarizer(full_text, max_length=130, min_length=30, do_sample=False)
            st.subheader("🧠 Emotional Summary")
            st.markdown(summary[0]['summary_text'])
    except Exception as e:
        st.error(f"❌ Eroare la generarea rezumatului: {e}")
