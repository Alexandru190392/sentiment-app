import streamlit as st

st.set_page_config(page_title="ReflectAI", page_icon="🧠", layout="centered")

st.title("🧠 ReflectAI")
st.write("Bine ai venit în aplicația ReflectAI! 👇\n\nFolosește meniul din stânga pentru a începe:")
st.markdown("- 🔐 Autentificare\n- 📓 Jurnal Emoțional\n- 🤖 ReflectAI")

if "utilizator" in st.session_state:
    st.success(f"Conectat ca: **{st.session_state.utilizator}**")
else:
    st.warning("Nu ești autentificat momentan.")
