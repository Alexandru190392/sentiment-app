import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import os

def extract_emotion(text):
    # Înlocuiește cu un model real sau o analiză mai sofisticată
    if "fericit" in text.lower():
        return "Fericire"
    elif "trist" in text.lower():
        return "Tristețe"
    elif "nervos" in text.lower():
        return "Furie"
    elif "calm" in text.lower():
        return "Calm"
    elif "stresat" in text.lower():
        return "Stres"
    else:
        return "Neutru"

def load_emotions_from_journal(file_path="jurnal_salvat.txt"):
    if not os.path.exists(file_path):
        return pd.DataFrame(columns=["timestamp", "emotion"])

    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n\n")
        for entry in lines:
            if entry.strip():
                try:
                    timestamp_str = entry.split("]")[0][1:]
                    text = entry.split("]")[1].strip()
                    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
                    emotion = extract_emotion(text)
                    data.append({"timestamp": timestamp, "emotion": emotion})
                except:
                    continue

    return pd.DataFrame(data)

def show_emotion_chart(df, period="week"):
    if df.empty:
        return "📭 Nu există date încă. Scrie ceva în jurnal mai întâi."

    now = datetime.now()

    if period == "day":
        cutoff = now - timedelta(days=1)
    elif period == "week":
        cutoff = now - timedelta(days=7)
    else:
        cutoff = now - timedelta(days=30)

    df_filtered = df[df["timestamp"] >= cutoff]
    if df_filtered.empty:
        return "📭 Nicio emoție înregistrată în această perioadă."

    emotion_counts = df_filtered["emotion"].value_counts()

    fig, ax = plt.subplots()
    emotion_counts.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_title("Frecvența emoțiilor")
    ax.set_ylabel("Număr apariții")
    ax.set_xlabel("Emoție")

    return fig
