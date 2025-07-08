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
    pipeline_available = True
except Exception:
    pipeline_available = False
    st.error("❌ Eroare la încărcarea pachetului 'transformers'.")

if pipeline_available:
    try:
        sentiment_analyzer = pipeline("sentiment-analysis", device=-1)
    except Exception:
        sentiment_analyzer = None
        st.error("❌ Eroare la inițializarea analizei de sentiment.")

    try:
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception:
        summarizer = None
        st.error("❌ Eroare la inițializarea sumarizatorului.")
else:
    sentiment_analyzer = None
    summarizer = None

try:
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding_model = embedding_model.to(torch.device("cpu"))
except Exception:
    embedding_model = None
    st.error("❌ Eroare la inițializarea modelului de similaritate.")

# === FUNCȚII ===
def analizeaza_sentimentul(text):
    if sentiment_analyzer:
        return sentiment_analyzer(text)
    else:
        return [{"label": "N/A", "score": 0.0}]

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

def find_similar_entry(current_text, similarity_threshold=0.8):
    if embedding_model is None:
        return None
    current_vector = embedding_model.encode(current_text)
    if not os.path.exists("journal_entries.json"):
        return None
    with open("journal_entries.json", "r", encoding="utf-8") as f:
        lines = f.readlines()
    most_similar, highest_similarity = None, 0
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

def genereaza_rezumat_emotional():
    try:
        if not summarizer:
            st.error("❌ Funcția de rezumat nu este disponibilă.")
            return
        if not os.path.exists("journal_entries.json"):
            st.warning("Nu există date salvate.")
            return
        with open("journal_entries.json", "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not lines:
            st.info("Jurnalul este gol.")
            return
        full_text = "\n".join([json.loads(line)["text"] for line in lines])
        full_text = full_text[:3000]
        summary = summarizer(full_text, max_length=130, min_length=30, do_sample=False)
        st.subheader("🧠 Emotional Summary")
        st.markdown(summary[0]['summary_text'])
    except Exception as e:
        st.error(f"Eroare la generarea rezumatului: {e}")

def deep_research():
    try:
        if not os.path.exists("journal_entries.json"):
            st.info("Nu există date salvate.")
            return
        with open("journal_entries.json", "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f.readlines()]
        if not data:
            st.info("Jurnalul este gol.")
            return
        df = pd.DataFrame([{
            "timestamp": entry["timestamp"],
            "score": entry["result"][0]["score"],
            "label": entry["result"][0]["label"],
            "text": entry["text"]
        } for entry in data])
        st.subheader("📊 Distribuția emoțională")
        st.bar_chart(df["label"].value_counts())
        st.subheader("🔍 Insights")
        st.markdown(f"**Scor mediu:** {df['score'].mean():.3f}")
        st.markdown(f"**Ziua cea mai pozitivă:** {df.loc[df['score'].idxmax()]['timestamp']}")
        st.markdown(f"**Ziua cea mai negativă:** {df.loc[df['score'].idxmin()]['timestamp']}")
        words = re.findall(r"\b\w{4,}\b", " ".join(df["text"]).lower())
        common_words = Counter(words).most_common(5)
        st.subheader("🧠 Cele mai frecvente 5 cuvinte")
        for word, freq in common_words:
            st.write(f"{word} — {freq} ori")
    except Exception as e:
        st.error(f"A apărut o eroare: {e}")

# === INTERFAȚĂ STREAMLIT ===
st.title("🔍 Analiză Sentiment - Demo Alexandru Florin Drăghici")

if st.button("📈 Vezi graficul"):
    afiseaza_grafic_sentimente()

text_input = st.text_area("✏️ Introdu textul pentru analiză:")
if st.button("🔍 Analizează"):
    if text_input:
        rezultat = analizeaza_sentimentul(text_input)
        st.success(f"Etichetă: {rezultat[0]['label']} — Scor: {rezultat[0]['score']:.4f}")
        salveaza_rezultatul(text_input, rezultat)
        feedback = st.radio("📊 A fost utilă analiza?", ["Da", "Nu"])
        if st.button("📤 Trimite feedback"):
            adauga_feedback(feedback)
            st.info("✅ Feedback salvat.")
    else:
        st.warning("⚠️ Introdu un text.")

st.header("📓 Jurnal Emoțional")
with st.form("journal_form"):
    tema_zilei = st.text_input("Temă opțională:")
    text_jurnal = st.text_area("Scrie aici:", height=300)
    submit = st.form_submit_button("📝 Salvează jurnal")
if submit and text_jurnal.strip():
    rezultat = analizeaza_sent_
