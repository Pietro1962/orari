import json
import urllib.request
from datetime import datetime

# Elenco dei 12 calendari UP Cineca A.A. 2026/2027
CALENDARI = [
    {"sheet": "Economia I", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 1, "anno": "1° anno", "color": "#1e3a8a", "id": "6a63231e7e6b9600bbc5fd93"},
    {"sheet": "Economia II", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 2, "anno": "2° anno", "color": "#1e40af", "id": "6a632535aae8aa00b5594f76"},
    {"sheet": "Economia III", "cdl_code": "ECONOMIA", "cdl_name": "CdL Triennale in Economia", "cdl_type": "Triennale", "year_order": 3, "anno": "3° anno", "color": "#1d4ed8", "id": "6a632799de54e8007a24a1a0"},
    {"sheet": "SDS I", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 1, "anno": "1° anno", "color": "#065f46", "id": "6a63238b7e6b9600bbc5fdc1"},
    {"sheet": "SDS II", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 2, "anno": "2° anno", "color": "#047857", "id": "6a63257e9e36710014cd0620"},
    {"sheet": "SDS III", "cdl_code": "SDS", "cdl_name": "CdL Triennale in Statistica per Data Science", "cdl_type": "Triennale", "year_order": 3, "anno": "3° anno", "color": "#059669", "id": "6a6327d4de54e8007a24a1d0"},
    {"sheet": "EIS I", "cdl_code": "EIS", "cdl_name": "CdL Magistrale in Economia, Imprese e Sostenibilità", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#9a3412", "id": "6a632453de54e8007a24a06c"},
    {"sheet": "EIS II", "cdl_code": "EIS", "cdl_name": "CdL Magistrale in Economia, Imprese e Sostenibilità", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#c2410c", "id": "6a632663acb9d70071d051e4"},
    {"sheet": "DSSA I", "cdl_code": "DSSA", "cdl_name": "CdL Magistrale in Data Science per le Strategie Aziendali", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#6b21a8", "id": "6a6323ea7bf6a400143cf32a"},
    {"sheet": "DSSA II", "cdl_code": "DSSA", "cdl_name": "CdL Magistrale in Data Science per le Strategie Aziendali", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#7e22ce", "id": "6a6325d84a2373001968598c"},
    {"sheet": "Finance I", "cdl_code": "FINANCE", "cdl_name": "CdL Magistrale in Finance and Insurance", "cdl_type": "Magistrale", "year_order": 1, "anno": "1° anno", "color": "#831843", "id": "6a6324b3b0e7470014a6276b"},
    {"sheet": "Finance II", "cdl_code": "FINANCE", "cdl_name": "CdL Magistrale in Finance and Insurance", "cdl_type": "Magistrale", "year_order": 2, "anno": "2° anno", "color": "#9f1239", "id": "6a6326b34a237300196859e1"}
]

all_lessons = []

for cal in CALENDARI:
    url = f"https://unical.prod.up.cineca.it/api/CalendarioPubblico/getEventiCalendarioPubblico?linkCalendarioId={cal['id']}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            eventi = data.get('eventi', []) if isinstance(data, dict) else []
            for ev in eventi:
                # Estrazione e pulizia campi
                materia = ev.get('insegnamento', ev.get('title', 'Lezione'))
                docente = ev.get('docente', ev.get('docenti', 'Docente da definire'))
                aula = ev.get('aula', ev.get('aule', 'Aula TBD'))
                
                # Conversione orari e giorni
                start_dt = datetime.fromisoformat(ev['start'].replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(ev['end'].replace('Z', '+00:00'))
                
                giorni_map = {0: 'Lunedì', 1: 'Martedì', 2: 'Mercoledì', 3: 'Giovedì', 4: 'Venerdì', 5: 'Sabato', 6: 'Domenica'}
                giorno_ita = giorni_map.get(start_dt.weekday(), '')
                orario_str = f"{start_dt.strftime('%H:%M')} - {end_dt.strftime('%H:%M')}"
                
                lesson_obj = {
                    "sheet": cal["sheet"],
                    "cdl_code": cal["cdl_code"],
                    "cdl_name": cal["cdl_name"],
                    "cdl_type": cal["cdl_type"],
                    "year_order": cal["year_order"],
                    "anno": cal["anno"],
                    "color": cal["color"],
                    "giorno": giorno_ita,
                    "orario": orario_str,
                    "materia": materia,
                    "docente": docente,
                    "aula": aula
                }
                all_lessons.append(lesson_obj)
    except Exception as e:
        print(f"Errore recupero {cal['sheet']}: {e}")

# Salva i dati scaricati nel file JSON
with open('lessons_data.json', 'w', encoding='utf-8') as f:
    json.dump(all_lessons, f, ensure_ascii=False, indent=4)

print(f"Recuperati con successo {len(all_lessons)} eventi da CINECA.")