import streamlit as st

st.set_page_config(page_title="ReflectAI", page_icon="🧠", layout="centered")

st.title("🧠 ReflectAI")
st.markdown("Bine ai venit în aplicația ReflectAI!\n\n👉 Folosește meniul din stânga pentru a începe:")

if "utilizator" in st.session_state:
    st.success(f"✅ Conectat ca: **{st.session_state.utilizator}**")
else:
    st.warning("🔐 Nu ești autentificat. Mergi la pagina ReflectAI Autentificare.")
