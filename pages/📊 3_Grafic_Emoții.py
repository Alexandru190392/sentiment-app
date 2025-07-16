import streamlit as st
from emotion_chart import load_emotions_from_journal, show_emotion_chart

st.set_page_config(page_title="Grafic Emoțional", page_icon="📊")

st.title("📊 Grafic Emoțional")
st.markdown("Analizează cum s-au schimbat emoțiile tale de-a lungul timpului.")

df = load_emotions_from_journal()

optiune = st.selectbox("📆 Alege perioada", ["Ziua de azi", "Ultima săptămână", "Ultima lună"])

if optiune == "Ziua de azi":
    period = "day"
elif optiune == "Ultima săptămână":
    period = "week"
else:
    period = "month"

fig = show_emotion_chart(df, period)
if isinstance(fig, str):
    st.warning(fig)
else:
    st.pyplot(fig)
