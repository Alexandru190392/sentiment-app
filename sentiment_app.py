import streamlit as st
import time

# 🧠 Configurare generală a aplicației
st.set_page_config(
    page_title="ReflectAI - Jurnalul Emoțional Inteligent",
    page_icon="🧠",
    layout="centered"
)

# 🔐 Redirecționare dacă utilizatorul nu e autentificat
if "utilizator" not in st.session_state:
    st.info("🔐 Redirecționare către autentificare...")
    time.sleep(1)
    st.switch_page("pages/1_ReflectAI_Autentificare.py")

# ✅ Dacă este autentificat, afișăm interfața principală
st.markdown("<h1 style='text-align: center; color: #5A4FCF;'>🧠 ReflectAI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Jurnalul Emoțional Inteligent</h3>", unsafe_allow_html=True)

st.divider()

# ✨ Mesaj de impact
st.markdown("""
> *„În fiecare zi, purtăm cu noi gânduri nespuse, emoții neînțelese și dorința de a ne cunoaște mai bine.”*

ReflectAI este mai mult decât o aplicație – este oglinda ta interioară.

📓 Scrie în jurnal.  
📊 Înțelege-ți emoțiile.  
🌱 Evoluează zi de zi.
""")

# 🙌 Bine ai venit
st.success(f"Bine ai revenit, **{st.session_state.utilizator}**! Te așteptăm în jurnalul tău.")

# 🔗 Instrucțiuni de navigare
st.markdown("""
---

### 🔍 Folosește meniul din stânga pentru a începe:
- **📓 Jurnal Emoțional** – scrie și analizează
- **🧠 ReflectAI** – vezi analiza pe text
- **🔐 Autentificare** – schimbă utilizatorul

""")
