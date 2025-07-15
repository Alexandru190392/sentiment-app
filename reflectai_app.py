import streamlit as st

st.set_page_config(page_title="ReflectAI", page_icon="🧠", layout="centered")

st.title("🧠 ReflectAI – Jurnal Emoțional")

if "utilizator" in st.session_state:
    st.success(f"Bine ai revenit, {st.session_state['utilizator']}!")
    st.markdown("📓 Poți accesa jurnalul tău emoțional din bara din stânga.")
else:
    st.info("🔐 Te rugăm să te autentifici din pagina de **Autentificare** din meniul din stânga.")
