import time
import streamlit as st
import json
import hashlib
import os

USERS_FILE = "utilizatori.json"

def incarca_utilizatori():
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            continut = f.read().strip()
            if not continut:
                return {}
            utilizatori = json.loads(continut)
            if not isinstance(utilizatori, dict):
                return {}
            return utilizatori
    except Exception:
        return {}

def salveaza_utilizatori(utilizatori):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(utilizatori, f, ensure_ascii=False, indent=2)

def hash_parola(parola):
    return hashlib.sha256(parola.encode()).hexdigest()

def creeaza_cont(nume, parola, confirmare):
    utilizatori = incarca_utilizatori()
    if nume in utilizatori:
        return False, "Acest nume de utilizator este deja luat."
    if parola != confirmare:
        return False, "Parolele nu se potrivesc."
    utilizatori[nume] = hash_parola(parola)
    salveaza_utilizatori(utilizatori)
    return True, "Cont creat cu succes!"

def autentificare(nume, parola):
    utilizatori = incarca_utilizatori()
    if nume not in utilizatori:
        return False, "Acest cont nu există."
    if utilizatori[nume] != hash_parola(parola):
        return False, "Parolă incorectă."
    return True, "Autentificare reușită."

# === UI ===
st.set_page_config(page_title="ReflectAI Autentificare", page_icon="🔐")

pagina = st.session_state.get("pagina_start", "Crează cont")
pagina = st.sidebar.radio("🔑 Alege acțiunea:", ["Crează cont", "Autentificare"], index=0 if pagina == "Crează cont" else 1)

if pagina == "Crează cont":
    st.subheader("🆕 Creare cont nou")
    nume = st.text_input("👤 Nume utilizator")
    parola = st.text_input("🔒 Parolă", type="password")
    confirmare = st.text_input("🔒 Confirmă parola", type="password")
    if st.button("✅ Creează cont"):
        succes, mesaj = creeaza_cont(nume, parola, confirmare)
        if succes:
            st.success(mesaj)
        else:
            st.error(mesaj)

elif pagina == "Autentificare":
    st.subheader("🔑 Autentificare")
    nume = st.text_input("👤 Nume utilizator")
    parola = st.text_input("🔒 Parolă", type="password")
    if st.button("🔓 Autentifică-te"):
        succes, mesaj = autentificare(nume, parola)
        if succes:
            st.success(f"Bine ai revenit, **{nume}**! Mergi spre jurnalul tău.") 
            time.sleep(1)
            st.switch_page("pages/2_Jurnal_Emotional.py")
        else:
            st.error(mesaj)

# === Status sesiune ===
if "utilizator" in st.session_state:
    st.sidebar.success(f"Ești logat ca: {st.session_state.utilizator}")
