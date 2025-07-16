import streamlit as st

st.set_page_config(page_title="ReflectAI", page_icon="🧠", layout="centered")

# Dacă utilizatorul e deja logat
if "utilizator" in st.session_state:
    st.switch_page("pages/2_Jurnal_Emotional.py")

st.title("🧠 ReflectAI")
st.subheader("Jurnalul Emoțional Inteligent")

st.markdown("""
**ReflectAI** este mai mult decât o aplicație – este oglinda ta interioară.  
Un spațiu sigur, profund și evolutiv:

- 📝 Scrii în jurnal.  
- 📊 Îți înțelegi emoțiile în timp real.  
- 🌱 Evoluezi zilnic prin introspecție.
""")

st.warning("Nu ești autentificat.")
st.markdown("👇 Alege una din opțiunile de mai jos pentru a începe:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔐 Autentificare"):
        st.switch_page("pages/1_ReflectAI_Autentificare.py")

with col2:
    if st.button("🆕 Crează cont"):
        st.switch_page("pages/1_ReflectAI_Autentificare.py")
