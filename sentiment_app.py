import streamlit as st

st.set_page_config(page_title="ReflectAI", page_icon="🧠", layout="centered")

st.title("🧠 ReflectAI App")
st.markdown("Aplicația funcționează! ✅")

if "utilizator" in st.session_state:
    st.success(f"Conectat ca: **{st.session_state.utilizator}**")
else:
    st.warning("🔐 Nu ești autentificat.")
