import streamlit as st
from datetime import datetime

# Aplicație cu stil similar ReflectAI
st.markdown("""
    <style>
        .stApp {
            background-color: #F6F8FC;
        }

        h1 {
            color: #5A4FCF;
            font-size: 2.8em;
            text-align: center;
        }

        .intro {
            text-align: center;
            font-size: 1.1em;
            margin-bottom: 2em;
            color: #555;
        }

        .journal-box {
            background-color: white;
            padding: 2em;
            border-radius: 15px;
            max-width: 700px;
            margin: auto;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
        }

        .result-box {
            background-color: #EAF5EA;
            padding: 1.2em;
            border-left: 6px solid #4CAF50;
            margin-top: 1.5em;
            border-radius: 10px;
            color: #2E7D32;
        }
    </style>
""", unsafe_allow_html=True)

# Titlu și introducere
st.markdown("<h1>📘 Jurnal Emoțional</h1>", unsafe_allow_html=True)
st.markdown('<p class="intro">Scrie ce simți. Reflectă. Află ce emoții trăiești.</p>', unsafe_allow_html=True)

# Cutia de jurnal completă cu Titlul zilei
with st.form("jurnal_form"):
    st.markdown('<div class="journal-box">', unsafe_allow_html=True)
    titlu = st.text_input("📅 Titlul zilei")
    text_input = st.text_area("✍️ Ce s-a întâmplat azi în viața ta?", height=200)
    submitted = st.form_submit_button("🔍 Analizează")
    st.markdown('</div>', unsafe_allow_html=True)

# Emoții simple
pozitive = ["fericit", "recunoscător", "iubire", "mândru", "entuziasm", "calm", "liniște"]
negative = ["trist", "supărat", "nervos", "confuz", "singur", "anxios", "obosit"]

def analiza_text(text):
    cuvinte = text.lower().split()
    total = len(cuvinte)
    poz = sum(c in pozitive for c in cuvinte)
    neg = sum(c in negative for c in cuvinte)
    poz_pct = round(poz / total * 100, 1) if total > 0 else 0
    neg_pct = round(neg / total * 100, 1) if total > 0 else 0
    return poz_pct, neg_pct, total

# Afișare analiză și salvare
if submitted and text_input.strip() != "":
    poz_pct, neg_pct, total = analiza_text(text_input)

    # Feedback personalizat
    mesaj = "💪 Felicitări, faci progrese!" if poz_pct > 50 else "🌧️ Niciuna dintre zile nu e la fel. Continuă să scrii."
    
    # Afișare rezultat
    st.markdown(f"""
        <div class="result-box">
            <b>Analiză:</b><br>
            Total cuvinte: {total}<br>
            Emoții pozitive: {poz_pct}%<br>
            Emoții negative: {neg_pct}%<br><br>
            {mesaj}
        </div>
    """, unsafe_allow_html=True)

    # Salvare jurnal
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("jurnal_salvat.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] TITLU: {titlu}\n{text_input}\n\n")

# Dacă a fost trimis jurnalul
if submitted and text_input.strip() != "":
    # Simulare analiză emoțională (înlocuiește cu analiza reală mai târziu)
    st.markdown("""
        <div class="result-box">
            ✅ Jurnal salvat! Ai menționat multe elemente pozitive. S-ar putea să te simți <b>recunoscător</b> și <b>optimist</b> azi.
        </div>
    """, unsafe_allow_html=True)

    # (Opțional) Salvare locală:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open("jurnal_salvat.txt", "a", encoding="utf-8") as f:
        f.write(f"[{now}] {text_input}\n\n")
