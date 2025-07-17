import streamlit as st
from emotion_chart import load_emotions_from_journal, show_emotion_chart
import json
import streamlit as st

# === Încărcare roata emoțiilor în română ===
with open("emotii_romana.json", "r", encoding="utf-8") as f:
    roata_emotii = json.load(f)

st.markdown("## 🌈 Explorare Emoții")
st.write("Selectează emoțiile pentru a reflecta mai profund asupra stării tale.")

# === Selecție în 3 niveluri ===
emoție_principală = st.selectbox("1. Emoție de bază", list(roata_emotii.keys()))
subemoții = list(roata_emotii[emoție_principală].keys())
emoție_secundară = st.selectbox("2. Emoție intermediară", subemoții)
detalii = roata_emotii[emoție_principală][emoție_secundară]
emoție_finală = st.selectbox("3. Emoție detaliată", detalii)

# Afișare rezultat
st.success(f"✅ Emoția ta selectată este: **{emoție_finală}**")

st.set_page_config(page_title="Grafic Emoțional", page_icon="📊")

st.title("📊 Grafic Emoțional")
st.markdown("Analizează cum s-au schimbat emoțiile tale de-a lungul timpului.")

# ✅ Verifică autentificarea
if "utilizator" not in st.session_state:
    st.warning("🔒 Trebuie să fii autentificat pentru a vedea graficul emoțional.")
    st.stop()

current_user = st.session_state["utilizator"]

# ✅ Încarcă jurnalul pentru utilizatorul curent
df = load_emotions_from_journal(current_user)

# ✅ Verifică dacă există date
if df.empty:
    st.warning("📭 Nu există date încă. Scrie ceva în jurnal mai întâi.")
    st.stop()

# ✅ Selectare perioadă
optiune = st.selectbox("📆 Alege perioada", ["Ziua de azi", "Ultima săptămână", "Ultima lună"])

if optiune == "Ziua de azi":
    period = "day"
elif optiune == "Ultima săptămână":
    period = "week"
else:
    period = "month"

# ✅ Afișează graficul
fig = show_emotion_chart(df, period)
st.pyplot(fig)
