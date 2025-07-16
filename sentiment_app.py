import streamlit as st

st.set_page_config(page_title="ReflectAI", page_icon="🧠", layout="centered")

if "utilizator" not in st.session_state:
    st.info("🔐 Te rugăm să te autentifici din pagina de 'ReflectAI Autentificare'.")
    st.stop()

st.title("🧠 ReflectAI - Sentiment App")
st.success(f"Bine ai venit, {st.session_state.utilizator}!")
