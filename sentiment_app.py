import streamlit as st
import time

st.set_page_config(page_title="ReflectAI - Jurnalul Emoțional Inteligent", page_icon="🧠", layout="centered")

# ✅ TITLU & PREZENTARE – mereu vizibil
st.markdown("<h1 style='text-align: center; color: #5A4FCF;'>🧠 ReflectAI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Jurnalul Emoțional Inteligent</h3>", unsafe_allow_html=True)
st.divider()

st.markdown("""
> *„În fiecare zi, purtăm cu noi gânduri nespuse, emoții neînțelese și dorința de a ne cunoaște mai bine.”*

ReflectAI este mai mult decât o aplicație – este oglinda ta interioară.

📓 Scrie în jurnal.  
📊 Înțelege-ți emoțiile.  
🌱 Evoluează zi de zi.
""")

st.divider()

# 🔄 Conținut diferit în funcție de autentificare:
if "utilizator" in st.session_state:
    st.success(f"Bine ai revenit, **{st.session_state.utilizator}**! Te așteptăm în jurnalul tău.")
else:
    st.warning("⚠️ Nu ești autentificat.")
    st.markdown("👇 Apasă mai jos pentru a te conecta la jurnal:")
    if st.button("🔐 Autentifică-te aici"):
        st.switch_page("pages/1_ReflectAI_Autentificare.py")
