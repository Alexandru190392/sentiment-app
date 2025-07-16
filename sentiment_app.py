import streamlit as st
import time

st.set_page_config(page_title="ReflectAI - Jurnalul Emoțional Inteligent", page_icon="🧠", layout="centered")
if "utilizator" not in st.session_state:
    st.switch_page("pages/1_ReflectAI_Autentificare.py")

# === Culori ===
PRIMARY = "#5A4FCF"
BG_COLOR = "#F6F8FC"

# === Stil HTML customizat ===
st.markdown(f"""
    <style>
        .stApp {{
            background-color: {BG_COLOR};
        }}
        h1 {{
            color: {PRIMARY};
            font-size: 3em;
            text-align: center;
            margin-bottom: 0.2em;
        }}
        h3 {{
            text-align: center;
            font-weight: 400;
            color: #444;
            margin-top: 0;
        }}
        .quote {{
            font-style: italic;
            font-size: 1.1em;
            color: #555;
            text-align: center;
            margin-bottom: 2em;
        }}
        .info-box {{
            background-color: white;
            padding: 1.5em;
            border-radius: 15px;
            box-shadow: 0 0 10px rgba(0,0,0,0.05);
            margin: 1em auto;
            max-width: 600px;
        }}
        .info-box ul {{
            padding-left: 1.2em;
        }}
        section[data-testid="stSidebar"] {{
            background-color: #EFF2F8;
        }}
        .element-container:has(.stAlert-success) {{
            max-width: 600px;
            margin: auto;
        }}
    </style>
""", unsafe_allow_html=True)

# === Titlu + Subtitlu ===
st.markdown("<h1>🧠 ReflectAI</h1>", unsafe_allow_html=True)
st.markdown("<h3>Jurnalul Emoțional Inteligent</h3>", unsafe_allow_html=True)
st.markdown("<div class='quote'>„În fiecare zi, purtăm cu noi gânduri nespuse, emoții neînțelese și dorința de a ne cunoaște mai bine.”</div>", unsafe_allow_html=True)

# === Info box ===
st.markdown("""
<div class="info-box">
<p><strong>ReflectAI</strong> este mai mult decât o aplicație – este oglinda ta interioară. Un spațiu sigur, profund și evolutiv unde:</p>
<ul>
<li>📓 Scrii în jurnal.</li>
<li>📊 Înțelegi emoțiile tale în timp real.</li>
<li>🌱 Evoluezi zilnic prin introspecție.</li>
</ul>
</div>
""", unsafe_allow_html=True)

# === Autentificare ===
if "utilizator" in st.session_state:
    st.success(f"Bine ai revenit, **{st.session_state.utilizator}**! Te așteptăm în jurnalul tău.")
else:
    st.warning("⚠️ Nu ești autentificat.")
    st.markdown("👇 Apasă mai jos pentru a te conecta:")
    if st.button("🔐 Autentifică-te aici"):
        st.switch_page("pages/1_ReflectAI_Autentificare.py")
