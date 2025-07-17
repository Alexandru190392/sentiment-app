import os
import json
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def load_emotions_from_journal(username):
    filepath = f"jurnale/{username}_journal.json"

    if not os.path.exists(filepath):
        return pd.DataFrame()

    with open(filepath, "r", encoding="utf-8") as f:
        entries = json.load(f)

    if not entries:
        return pd.DataFrame()

    df = pd.DataFrame(entries)
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d %H:%M")

    # Simulăm un scor emoțional pe baza lungimii textului (provizoriu)
    df["scor"] = df["continut"].apply(lambda x: len(x.split()))

    return df


def show_emotion_chart(df, period):
    now = datetime.now()

    if period == "day":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start = now - timedelta(days=7)
    else:
        start = now - timedelta(days=30)

    df_filtered = df[df["data"] >= start]

    if df_filtered.empty:
        return "📭 Nu există înregistrări în această perioadă."

    df_grouped = df_filtered.groupby(df_filtered["data"].dt.date)["scor"].mean()

    fig, ax = plt.subplots()
    df_grouped.plot(kind="line", marker="o", ax=ax)
    ax.set_title("Evoluția scorului emoțional")
    ax.set_ylabel("Scor (nr. cuvinte)")
    ax.set_xlabel("Data")
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig
