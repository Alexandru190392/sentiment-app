import streamlit as st

# Redirecționează spre pagina ReflectAI Autentificare
st.switch_page("ReflectAI Autentificare")

st.markdown("""
    <h1 style='text-align: center;'>🧠 ReflectAI</h1>
    <h2 style='text-align: center;'>Jurnalul Emoțional Inteligent</h2>
    <p style='text-align: center; color: gray;'>
        „În fiecare zi, purtăm cu noi gânduri nespuse, emoții neînțelese și dorința de a ne cunoaște mai bine.”
    </p>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='background-color: #fff; padding: 20px; border-radius: 10px; max-width: 800px; margin: auto; box-shadow: 0 0 10px rgba(0,0,0,0.05);'>
        <p><b>ReflectAI</b> este mai mult decât o aplicație – este oglinda ta interioară. Un spațiu sigur, profund și evolutiv unde:</p>
        <ul>
            <li>📝 Scrii în jurnal.</li>
            <li>📊 Înțelegi emoțiile tale în timp real.</li>
            <li>🌀 Evoluezi zilnic prin introspecție.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 🔓 Alege o opțiune:", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🔐 Autentificare"):
        st.switch_page("1_ReflectAI_Autentificare.py")
with col2:
    if st.button("🆕 Creează cont"):
        st.switch_page("1_ReflectAI_Autentificare.py")
        st.session_state["pagina"] = "Crează cont"
