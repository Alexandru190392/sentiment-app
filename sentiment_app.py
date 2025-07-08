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

def init_embedding_model():
    global embedding_model
    try:
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as e:
        embedding_model = None
        st.warning("⚠️ Modelul de similaritate nu a fost încărcat. Funcția de comparare este dezactivată.")

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

def find_similar_entry(current_text, similarity_threshold=0.8):
    if embedding_model is None:
        init_embedding_model()
    if embedding_model is None:
        return None
    current_vector = embedding_model.encode(current_text)
    if not os.path.exists("journal_entries.json"):
        return None
    with open("journal_entries.json", "r", encoding="utf-8") as f:
        lines = f.readlines()
    most_similar = None
    highest_similarity = 0
    for line in lines:
        try:
            entry = json.loads(line)
            previous_vector = embedding_model.encode(entry["text"])
            similarity = 1 - cosine(current_vector, previous_vector)
            if similarity > highest_similarity and similarity >= similarity_threshold:
                highest_similarity = similarity
                most_similar = {
                    "timestamp": entry["timestamp"],
                    "label": entry["result"][0]["label"],
                    "score": entry["result"][0]["score"],
                    "similarity": similarity
                }
        except Exception:
            continue
    return most_similar

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

def deep_research():
    try:
        if not os.path.exists("journal_entries.json"):
            st.info("Nu există jurnal.")
            return
        with open("journal_entries.json", "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f.readlines()]
        df = pd.DataFrame([{
            "timestamp": e["timestamp"],
            "score": e["result"][0]["score"],
            "label": e["result"][0]["label"],
            "text": e["text"]
        } for e in data])
        st.subheader("📊 Distribuție emoțională")
        st.bar_chart(df["label"].value_counts())
        st.markdown(f"**Scor mediu:** {df['score'].mean():.3f}")
        st.markdown(f"**Ziua cea mai pozitivă:** {df.loc[df['score'].idxmax()]['timestamp']}")
        st.markdown(f"**Ziua cea mai negativă:** {df.loc[df['score'].idxmin()]['timestamp']}")
    except Exception as e:
        st.error(f"Eroare la analiză: {e}")

# === INTERFAȚĂ ===
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
    tema = st.text_input("Optional: Today's topic")
    jurnal_text = st.text_area("Scrie ce simți:", height=300)
    submit = st.form_submit_button("📝 Salvează jurnal")
if submit and jurnal_text.strip():
    rezultat = analizeaza_sentimentul(jurnal_text)
    salveaza_intrare_jurnal(jurnal_text, rezultat, tema)
    similar = find_similar_entry(jurnal_text)
    if similar:
        st.warning(f"Similar cu ziua: {similar['timestamp']} — {similar['label']} ({similar['similarity']:.2f})")
    st.success(f"✅ Jurnal salvat — {rezultat[0]['label']} ({rezultat[0]['score']:.4f})")

if st.button("🔎 Deep Research – Analyze your journal"):
    deep_research()

if st.button("🧠 Generate Emotional Summary"):
    genereaza_rezumat_emotional()
