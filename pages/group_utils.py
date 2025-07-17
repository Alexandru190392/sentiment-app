import streamlit as st
import json
import os

GRUP_FILE = "grupuri.json"

# → Helper pentru incărcare/salvare

def incarca_grupuri():
    if not os.path.exists(GRUP_FILE):
        return {}
    with open(GRUP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def salveaza_grupuri(grupuri):
    with open(GRUP_FILE, "w", encoding="utf-8") as f:
        json.dump(grupuri, f, indent=2, ensure_ascii=False)

# → Creează un grup nou

def creeaza_grup(nume_grup, utilizator):
    grupuri = incarca_grupuri()
    if nume_grup in grupuri:
        return False, "Grupul deja există."
    grupuri[nume_grup] = {
        "admin": utilizator,
        "membri": [utilizator],
        "cereri": []
    }
    salveaza_grupuri(grupuri)
    return True, "Grup creat cu succes!"

# → Cerere de aderare

def cere_aderare(nume_grup, utilizator):
    grupuri = incarca_grupuri()
    if nume_grup not in grupuri:
        return False, "Grupul nu există."
    if utilizator in grupuri[nume_grup]["membri"]:
        return False, "Ești deja membru."
    if utilizator in grupuri[nume_grup]["cereri"]:
        return False, "Ai trimis deja o cerere."
    grupuri[nume_grup]["cereri"].append(utilizator)
    salveaza_grupuri(grupuri)
    return True, "Cerere trimisă. Așteaptă aprobarea."

# → Aprobare cerere de către admin

def aproba_cerere(nume_grup, utilizator, admin):
    grupuri = incarca_grupuri()
    if nume_grup not in grupuri:
        return False, "Grupul nu există."
    if grupuri[nume_grup]["admin"] != admin:
        return False, "Nu ai drept de aprobare."
    if utilizator not in grupuri[nume_grup]["cereri"]:
        return False, "Utilizatorul nu a cerut acces."
    grupuri[nume_grup]["cereri"].remove(utilizator)
    grupuri[nume_grup]["membri"].append(utilizator)
    salveaza_grupuri(grupuri)
    return True, "Utilizator aprobat cu succes."

# =========== INTERFAȚĂ DE TEST ===========

st.set_page_config(page_title="Grupuri ReflectAI", page_icon="👥")
st.title("👥 Test Grupuri ReflectAI")

if "utilizator" not in st.session_state:
    st.session_state["utilizator"] = "alexandru"  # simulare cont logat

utilizator = st.session_state["utilizator"]

st.subheader(f"Salut, {utilizator}!")

# 1. Creare grup
with st.expander("➕ Creează un grup nou"):
    nume_grup = st.text_input("Nume grup")
    if st.button("Creează grup"):
        ok, msg = creeaza_grup(nume_grup, utilizator)
        st.success(msg) if ok else st.error(msg)

# 2. Trimite cerere (simulează alt cont)
with st.expander("📨 Trimite cerere ca alt utilizator"):
    nume_grup = st.text_input("Grup pentru cerere", key="grup2")
    alt_user = st.text_input("Utilizator test", value="marius")
    if st.button("Trimite cerere"):
        ok, msg = cere_aderare(nume_grup, alt_user)
        st.success(msg) if ok else st.error(msg)

# 3. Aprobare de către admin
with st.expander("✅ Aprobă cerere de aderare"):
    nume_grup = st.text_input("Grup pentru aprobare", key="grup3")
    user_de_aprobat = st.text_input("Utilizator de aprobat", value="marius")
    if st.button("Aprobă"):
        ok, msg = aproba_cerere(nume_grup, user_de_aprobat, utilizator)
        st.success(msg) if ok else st.error(msg)

# 4. Vizualizare grupuri
with st.expander("📋 Vezi toate grupurile existente"):
    toate = incarca_grupuri()
    st.json(toate)
