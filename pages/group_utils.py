import json
import os

GRUPURI_FILE = "grupuri.json"

def incarca_grupuri():
    if not os.path.exists(GRUPURI_FILE):
        return []
    with open(GRUPURI_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def salveaza_grupuri(grupuri):
    with open(GRUPURI_FILE, "w", encoding="utf-8") as f:
        json.dump(grupuri, f, ensure_ascii=False, indent=2)

def adauga_grup(nume_grup, admin):
    grupuri = incarca_grupuri()
    for grup in grupuri:
        if grup["nume"] == nume_grup:
            return False  # grup deja existent
    grupuri.append({
        "nume": nume_grup,
        "admin": admin,
        "membri": [admin],
        "cereri": []
    })
    salveaza_grupuri(grupuri)
    return True

# Alte funcții (trimite_cerere, aproba_cerere etc.) le putem adăuga la cerere

def trimite_cerere(nume_grup, utilizator):
    grupuri = incarca_grupuri()
    if nume_grup not in grupuri:
        return False, "Grupul nu există."
    if utilizator in grupuri[nume_grup]["membri"]:
        return False, "Ești deja în acest grup."
    if utilizator in grupuri[nume_grup]["cereri"]:
        return False, "Cerere deja trimisă."
    grupuri[nume_grup]["cereri"].append(utilizator)
    salveaza_grupuri(grupuri)
    return True, "Cererea a fost trimisă."

def aproba_cerere(nume_grup, utilizator):
    grupuri = incarca_grupuri()
    if utilizator in grupuri[nume_grup]["cereri"]:
        grupuri[nume_grup]["cereri"].remove(utilizator)
        grupuri[nume_grup]["membri"].append(utilizator)
        salveaza_grupuri(grupuri)
        return True, "Utilizator aprobat."
    return False, "Cererea nu a fost găsită."
