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
except Exception as e:
    pipeline_available = False
    st.error("❌ Eroare la încărcarea pachetului 'transformers'.")

if pipeline_available:
    try:
        sentiment_analyzer = pipeline("sentiment-analysis", device=-1)
    except Exception as e:
        sentiment_analyzer = None
        st.error("❌ Eroare la inițializarea analizei de sentiment. Verifică pachetele 'transformers' și 'torch'.")
    try:
    except Exception as e:
        summarizer = None
        st.error("❌ Eroare la inițializarea sumarizatorului. Funcția de rezumat nu este disponibilă.")
else:
    sentiment_analyzer = None
    summarizer = None

try:
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding_model = embedding_model.to(torch.device("cpu"))
except Exception as e:
    embedding_model = None
    st.error("❌ Eroare la inițializarea modelului de similaritate. Funcția de comparare a jurnalelor va fi dezactivată.")

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

# === Sumarizare text ===
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def genereaza_rezumat_emotional():
    try:
        if not os.path.exists("journal_entries.json"):
            st.warning("No journal data found.")
            return

        with open("journal_entries.json", "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            st.info("Your journal is empty.")
            return

        full_text = "\n".join([json.loads(line)["text"] for line in lines])
        if len(full_text) > 3000:
            full_text = full_text[:3000]

        summary = summarizer(full_text, max_length=130, min_length=30, do_sample=False)

        st.subheader("🧠 Emotional Summary")
        st.markdown(summary[0]['summary_text'])

    except Exception as e:
        st.error(f"Something went wrong: {e}")

def deep_research():
    try:
        if not os.path.exists("journal_entries.json"):
            st.info("No journal data found.")
            return
        with open("journal_entries.json", "r", encoding="utf-8") as f:
            data = [json.loads(line) for line in f.readlines()]
        if not data:
            st.info("Journal is empty.")
            return
        df = pd.DataFrame([{
            "timestamp": entry["timestamp"],
            "score": entry["result"][0]["score"],
            "label": entry["result"][0]["label"],
            "text": entry["text"]
        } for entry in data])
        st.subheader("📊 Emotional distribution")
        st.bar_chart(df["label"].value_counts())
        st.subheader("🔍 Insights")
        st.markdown(f"**Average score:** {df['score'].mean():.3f}")
        st.markdown(f"**Most positive day:** {df.loc[df['score'].idxmax()]['timestamp']} — Score: {df['score'].max():.3f}")
        st.markdown(f"**Most negative day:** {df.loc[df['score'].idxmin()]['timestamp']} — Score: {df['score'].min():.3f}")
        all_text = " ".join(df["text"])
        words = re.findall(r"\b\w{4,}\b", all_text.lower())
        common_words = Counter(words).most_common(5)
        st.subheader("🧠 Top 5 most frequent words")
        for word, freq in common_words:
            st.write(f"{word} — {freq} times")
    except Exception as e:
        st.error(f"Something went wrong: {e}")

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
    text_jurnal = st.text_area("Write your thoughts here (as much as you want):", height=300)
    submit = st.form_submit_button("📝 Save Journal")
if submit and text_jurnal.strip():
    rezultat = analizeaza_sentimentul(text_jurnal)
    salveaza_intrare_jurnal(text_jurnal, rezultat, tema_zilei)
    similar_entry = find_similar_entry(text_jurnal)
    if similar_entry:
        st.warning(
            f"This journal entry is emotionally similar to what you wrote on "
            f"{similar_entry['timestamp'][:10]} (Label: {similar_entry['label']}, "
            f"Score: {similar_entry['score']:.2f}, Similarity: {similar_entry['similarity']:.2f})"
        )
    st.success(f"✅ Journal saved — Label: {rezultat[0]['label']}, Score: {rezultat[0]['score']:.4f}")

if st.button("🔎 Deep Research – Analyze your journal"):
    deep_research()

if st.button("🧠 Generate Emotional Summary"):
    genereaza_rezumat_emotional()
