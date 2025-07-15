import streamlit as st
import json
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === Funcții ===
def analizeaza_sentimentul(text):
    pozitive = ["bine", "fericit", "iubesc", "mândru", "curajos", "clar", "entuziasm", "excelent", "plăcut"]
    negative = ["trist", "obosit", "urăsc", "supărat", "dezamăgit", "confuz", "rău", "singur"]
    text = text.lower()
    score = sum(1 for w in text.split() if w in pozitive) - sum(1 for w in text.split() if w in negative)
    label = "Pozitiv" if score > 0 else "Negativ" if score < 0 else "Neutru"
    return [{"label": label, "score": round(abs(score) / max(1, len(text.split())), 2)}]

def salveaza_intrare(user, text, rezultat, tema=None):
    if not user:
        st.error("⚠️ Trebuie să fii autentificat!")
        return
    nume_fisier = f"journal_{user}.json"
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
    st.success("✅ Intrarea a fost salvată!")

def genereaza_rezumat(user):
    nume_fisier = f"journal_{user}.json"
    if not os.path.exists(nume_fisier):
        st.warning("Nu există jurnal pentru acest utilizator.")
        return
    with open(nume_fisier, "r", encoding="utf-8") as f:
        lines = f.readlines()
    text = "\n".join([json.loads(line)["text"] for line in lines])
    propoziții = re.split(r'[.!?]', text)
    summary = ". ".join(propoziții[:2]).strip() + "."
    st.subheader("🧠 Rezumat Emoțional (Logic)")
    st.markdown(summary)

def afiseaza_grafic(user):
    nume_fisier = f"journal_{user}.json"
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

def sterge_jurnal(user):
    nume_fisier = f"journal_{user}.json"
    if os.path.exists(nume_fisier):
        open(nume_fisier, "w", encoding="utf-8").close()
        st.warning("⚠️ Jurnalul a fost șters complet.")
    else:
        st.info("📂 Nu există jurnal pentru acest utilizator.")

# === Pagina principală jurnal ===
st.title("📓 Jurnal Emoțional – ReflectAI")

if "utilizator" not in st.session_state:
    st.warning("🔒 Te rugăm să te autentifici din pagina de 'Autentificare'.")
    st.stop()

user = st.session_state.utilizator

st.success(f"Bun venit, {user}!")

with st.form("jurnal_form"):
    tema = st.text_input("📝 Tema zilei (opțional)")
    text = st.text_area("✏️ Scrie ce simți:", height=300)
    trimite = st.form_submit_button("📝 Salvează jurnal")

if trimite and text.strip():
    rezultat = analizeaza_sentimentul(text)
    salveaza_intrare(user, text, rezultat, tema)

st.subheader("📈 Analizează Jurnalul Tău")
if st.button("🧠 Generează Rezumat Emoțional"):
    genereaza_rezumat(user)

if st.button("📊 Vezi Graficul Emoțiilor"):
    afiseaza_grafic(user)

if st.button("🗑️ Șterge Jurnalul"):
    sterge_jurnal(user)
