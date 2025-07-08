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

# === CACHED MODELS ===
@st.cache_resource
def load_sentiment_model():
    from transformers import pipeline
    return pipeline("sentiment-analysis")

@st.cache_resource
def load_summarizer_model():
    from transformers import pipeline
    return pipeline("summarization")

@st.cache_resource
def load_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

try:
    sentiment_analyzer = load_sentiment_model()
    summarizer = load_summarizer_model()
    embedding_model = load_embedding_model()
except Exception as e:
    sentiment_analyzer = None
    summarizer = None
    embedding_model = None
    st.error("❌ Eroare la încărcarea pachetelor 'transformers' sau la inițializare.")

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
