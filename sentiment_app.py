import streamlit as st

st.set_page_config(page_title="ReflectAI", page_icon="🧠", layout="centered")

if "utilizator" not in st.session_state:
    st.warning("⚠️ Nu ești autentificat.")
    if st.button("🔐 Autentifică-te aici"):
        st.switch_page("pages/1_ReflectAI_Autentificare.py")
    st.stop()

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

st.success(f"Bine ai revenit, **{st.session_state.utilizator}**! Te așteptăm în jurnalul tău.")

st.markdown("""
---

### 🔍 Folosește meniul din stânga pentru a începe:
- **📓 Jurnal Emoțional** – scrie și analizează
- **🧠 ReflectAI** – vezi analiza pe text
- **🔐 Autentificare** – schimbă utilizatorul
""")
