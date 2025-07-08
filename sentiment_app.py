import os
import json
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.spatial.distance import cosine

# === MODEL SIMPLU DE TEST ===
sentiment_analyzer = None
embedding_model = None
summarizer = None

# === FUNCȚII ===

def analizeaza_sentimentul(text):
    text = text.lower()
    if "fericit" in text or "bine" in text or "superb" in text:
        return [{"label": "POSITIVE", "score": 0.9}]
    elif "trist" in text or "rău" in text or "nasol" in text:
        return [{"label": "NEGATIVE", "score": 0.9}]
    else:
        return [{"label": "NEUTRAL", "score": 0.5}]

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
    return None  # Temporar dezactivat

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
