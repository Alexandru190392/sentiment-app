import streamlit as st
from emotion_chart import load_emotions_from_journal, show_emotion_chart

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
