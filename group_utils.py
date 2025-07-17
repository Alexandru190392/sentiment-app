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

def trimite_cerere(nume_grup, utilizator):
    grupuri = incarca_grupuri()
    for grup in grupuri:
        if grup["nume"] == nume_grup:
            if utilizator in grup["membri"]:
                return False, "Ești deja în acest grup."
            if utilizator in grup["cereri"]:
                return False, "Cererea a fost deja trimisă."
            grup["cereri"].append(utilizator)
            salveaza_grupuri(grupuri)
            return True, "Cererea a fost trimisă."
    return False, "Grupul nu a fost găsit."

def aproba_cerere(nume_grup, utilizator):
    grupuri = incarca_grupuri()
    for grup in grupuri:
        if grup["nume"] == nume_grup:
            if utilizator in grup["cereri"]:
                grup["cereri"].remove(utilizator)
                grup["membri"].append(utilizator)
                salveaza_grupuri(grupuri)
                return True, "Utilizatorul a fost aprobat."
            return False, "Cererea nu a fost găsită."
    return False, "Grupul nu a fost găsit."
